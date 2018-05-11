from uuid import uuid4
from json import dumps


import cv2

import storyboard
from camera import Camera

camera = Camera()
image = camera.preview()
fname = 'images/' + str(uuid4()) + '.png'

cv2.imwrite(fname, image)

page = storyboard.Page(fname)
page.process(True)

data = dumps(page.export_json())

with open('data/curr_file.txt', 'w') as f:
    f.write(fname)
with open('data/data.json', 'w') as f:
    f.write(data)
with open('app/src/common/data.json', 'w') as f:
    f.write(data)