from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import deque, defaultdict


counter = 0


def set_global():
    global counter
    counter = 0


def it_gloabl():
    global counter
    counter +=1


def open_image(path):
    image = Image.open(path)
    return image


def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image


def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:
        return None

    pixel = image.getpixel((i,j))
    return pixel


def grayscale(image):
    width, height = image.size

    new = create_image(width,height)
    pixels = new.load()

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            gray = (red*0.299) + (green * 0.587) + (blue * 0.144)

            pixels[i,j] = (int(gray), int(gray), int(gray))

    return new


def black_white(image):
    width, height = image.size
    new = create_image(width, height)
    pixels = new.load()

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            if pixel[0]>175 and pixel[1]>175 and pixel[2]>175:
                pixels[i,j] = (255,255,255)
            else:
                pixels[i,j] = (0,0,0)

    return new


def check_existence(lines, position):
    exists = 0
    for l in lines:
        if position in l:
            exists += 1
        else:
            exists += 0
    if exists == 0:
        return False
    else:
        return True


def process(image):
    width, height = image.size
    lines = []
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            # for first line
            position = (i, j)
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                if len(lines) == 0:
                    line = line_find(image, list(position))
                    lines.append(line)
                elif not check_existence(lines, position):
                    line = line_find(image, list(position))
                    lines.append(line)
                else:
                    continue
    return lines


def line_find(img, start):
    black_list = set()
    queue = deque()
    queue.append(start)

    while len(queue) > 0:
        # check eight surrounding pixels
        for x in range(-1, 2):
            for y in range(-1, 2):
                # exclude self
                if x != 0 or y != 0:
                    # get pixel obj
                    nx = queue[0][0] + x
                    ny = queue[0][1] + y
                    pos = [nx, ny]
                    pixel = get_pixel(img, pos[0], pos[1])
                    # if pixel is black
                    if pixel[0] == 0:
                        if tuple(pos) not in black_list and queue.count(pos) == 0:
                            queue.append(pos)
        black_list.add(tuple(queue.popleft()))
    return black_list


def main():

    img = Image.open('plswork.png')
    bw = black_white(img)
    result = process(bw)
    f = open('points.txt', 'w')
    width, height = bw.size

    # Write information to file to be read into maya
    for res in result:
        st = ""
        l = list(res)
        for r in range(0, len(res)):
            if r != len(res) -1:
                q = list(l[r])
                st += str(q[0])+","+str(q[1])+" "
            else:
                q = list(l[r])
                st += str(q[0])+","+str(q[1])
        f.write(st+"\n")
    f.write(str(width) + "," + str(height))
    f.close()



main()