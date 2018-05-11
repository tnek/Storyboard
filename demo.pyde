add_library('serial')

import subprocess
import os

starting_path = os.getcwd()

os.chdir(starting_path)
subprocess.call(['/usr/local/bin/python', 'test.py'])

from arduino_controls.serial import Controls

serial = Serial(this, Serial.list()[-1], 9600)

controls = Controls(serial)

print(os.getcwd())

fname = open('data/curr_file.txt', 'r').read()

WIN_WIDTH = 800
WIN_HEIGHT = 500

def setup():
    global stage
    stage = loadImage(fname)
    stage.resize(WIN_WIDTH, WIN_HEIGHT)
    size(WIN_WIDTH, WIN_HEIGHT)

curr_frame = 0
frames = ['', '-blur.png', '-gray.png', '-canny.png', '-dilated.png', '-wireframe.png']
titles = ['PHOTO', 'BLUR', 'GRAY', 'CANNY', 'DILATED', 'WIREFRAME']

def draw():
    control = controls.check()
    global curr_frame
    global stage
    if control:
        if control == 'LEFT':
            curr_frame -= 1
            if curr_frame < 0:
                curr_frame = 0
            stage = loadImage(fname + frames[curr_frame])
            stage.resize(WIN_WIDTH, WIN_HEIGHT)
        elif control == 'RIGHT':
            curr_frame += 1
            if curr_frame >= len(frames):
                curr_frame = len(frames) - 1
            stage = loadImage(fname + frames[curr_frame])
            stage.resize(WIN_WIDTH, WIN_HEIGHT)

    background(255)
    image(stage, 0, 0)
    textSize(33)
    fill(0)
    text(titles[curr_frame], 97, 100)
    textSize(32)
    fill(255)
    text(titles[curr_frame], 100, 100)

    if curr_frame == len(frames) - 1:
        textSize(32)
        text("To webapp", WIN_WIDTH - 150, WIN_HEIGHT - 100)