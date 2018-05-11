from json import loads, dumps
import np
import cv2
import math

def create_blank(width, height, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image


def sort_corners(coords):
    x_sorted = sorted(list(coord) for coord in coords)
    y_sorted = sorted(x_sorted[2:], key=lambda x:x[1])
    return np.array(x_sorted[:2] + y_sorted)

class Element(object):
    def __init__(self, coords):
        self.parent = None
        self.elements = []

        self.coords = coords
        self.calculate_dimensions()

    def calculate_dimensions(self):
        self.sorted_coords = sort_corners(self.coords)
        self.width = self.sorted_coords[3][0] - self.sorted_coords[0][0]
        self.height = self.sorted_coords[3][1] - self.sorted_coords[0][1]
        self.area = self.width * self.height

    def rec_straightening(self, parent = None):
        center = (self.width + self.coords[0][0], self.height + self.coords[0][1])

        M = cv2.getRotationMatrix2D(center, self.theta, 1)
        if parent is not None:
            self.coords = cv2.transform(np.array([self.coords]), parent)
        else:
            self.coords = cv2.transform(np.array([self.coords]), M)

        self.coords = self.coords.tolist()[0]
        x_coords = sorted(i[0] for i in self.coords)
        y_coords = sorted(i[1] for i in self.coords)

        self.coords = np.array([
            [x_coords[0], y_coords[3]],
            [x_coords[0], y_coords[0]],
            [x_coords[3], y_coords[0]],
            [x_coords[3], y_coords[3]],
        ])
        for child in self.elements:
            child.rec_straightening(M)
        self.calculate_dimensions()


        return M

    def export_json(self):
        return {
            'tag': 'div',
            'x': self.coords[0][0],
            'y': self.coords[0][1],
            'height': self.height,
            'width': self.width,
            'children': [e.export_json() for e in self.elements],
        }

def preprocessing(image, debug=False, fname=None):
    blur = cv2.GaussianBlur(image,(3,3),0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,10, 55, apertureSize=3)

    kernel = np.ones((2,10), np.uint8)
    d_im = cv2.dilate(edges, kernel, iterations=2)
    e_im = cv2.erode(d_im, kernel, iterations=2)

    if debug:
        cv2.imwrite(fname+"-blur.png", blur)
        cv2.imwrite(fname+"-gray.png", gray)
        cv2.imwrite(fname+"-canny.png", edges)
        cv2.imwrite(fname+"-dilated.png", e_im)

    return e_im

class Page(Element):
    def __init__(self, fname):
        self.fname = fname
        self.parent = None
        self.elements = []

    def process(self, draw_layers=False):
        image = cv2.imread(self.fname)
        h, w, channel = image.shape
        self.width = w
        self.height = h
        self.coords = np.array([[0, h], [w, h], [w, 0], [0, 0]])
        self.sorted_coords = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

        image = preprocessing(image, draw_layers, self.fname)

        im2, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        filtered_hierarchy = []

        for cnt in range(len(contours)):
            if True:#cv2.contourArea(contours[cnt]) > 10:
                rect = cv2.minAreaRect(contours[cnt])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                e = Element(box)
                e.theta = rect[2]
                boxes.append(e)
                filtered_hierarchy.append(hierarchy[0][cnt])


        for entry in range(len(filtered_hierarchy)):
            parent_index = filtered_hierarchy[entry][3]
            if parent_index == -1:
                self.elements.append(boxes[entry])
                boxes[entry].parent = self
            else:
                boxes[parent_index].elements.append(boxes[entry])
                boxes[entry].parent = boxes[parent_index]


        for item in self.elements:
            item.rec_straightening()

        if draw_layers:
            wireframe = create_blank(w, h)
#            cv2.drawContours(contours_img, contours, -1, (0,255,0), 3)

#            cv2.imwrite(self.fname+"-contours.png", contours_img)
#
            for element in boxes:
                cv2.drawContours(wireframe,[element.coords],0,(0,0,255),1)
#
            cv2.imwrite(self.fname+"-wireframe.png", wireframe)
            cv2.imwrite(self.fname+'-image.png', image)

    def export_json(self):
        return {
            'tag': 'div',
            'x': 0,
            'y': 720,
            'height': 720,
            'width': 1280,
            'parent': {
                'x': 0,
                'y': 0,
            },
            'children': [e.export_json() for e in self.elements],
        }


#s = Page("../images/test2.jpeg")
#s = Page("../images/f804707c-6ebd-4321-b3e8-b82089918e12.png")
#s = Page("../images/WechatIMG19.jpeg")
#s = Page("../images/sample.jpeg")
#s.process(draw_layers=True)
