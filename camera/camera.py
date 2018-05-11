import cv2
import serial

PORT = '/dev/cu.wchusbserial1420'


class Camera:

    def __init__(self):
        print('Camera Initialized')
        self._port = None
        try:
            port = serial.Serial(PORT, timeout=0)
            while True:
                port.flush()
                res = port.readline()
                port.writelines(['PING\n'])
                if len(res):
                    print('Received: %s' % res)
                if '[PONG]' in res:
                    break
            self._port = port
        except Exception as e:
            print(e)

    def preview(self):
        cv2.namedWindow('preview')
        index = 0
        vc = cv2.VideoCapture(index)

        frame = None

        rval = True
        frame = None
        while rval:
            if vc.isOpened(): # try to get the first frame
                rval, frame = vc.read()
            else:
                rval = False
            cv2.imshow("preview", frame)
            rval, frame = vc.read()
            key = cv2.waitKey(20)
            if key != -1:
                print(key)
            if key == 0: # UP
                cv2.clearCapture(vc)
                vc = cv2.VideoCapture(index + 1)
            elif key == 1: # DOWN
                cv2.clearCapture(vc)
                vc = cv2.VideoCapture(index - 1)
            elif key == 27: # exit on ESC, passing last frame
                rval = False
            if self._port:
                self._port.flush()
                res = self._port.read(1024)
                if 'RIGHT' in res:
                    break

        cv2.destroyWindow("preview")

        return frame