from PIL import Image
import numpy as np
from datetime import datetime as dt
import cv2

__author__ = "Sargassum Early Advisory System (SEAS) Team"
__date__ = "September 16, 2016"
__copyright__ = "Copyright 2016, Sargassum Early Advisory System"
__credits__ = ["Vaughn Linton", "Kyle Robertson", "Mike Wurl"]

__license__ = "MIT"
__version__ = "0.1"
__email__ = ["roberttk01@gmail.com", "redeyesmike@hotmail.com"]
__Status__ = "Production"

# Script developed to be utilized by the Sargassum Early Advisory System (SEAS) team for the low level analysis and
# detection of Sargassum in satellite imagery. Python3 libraries required include:
#   1) Pillow
#   2) numpy
#   3) opencv-python
#   4) datetime (native and only for testing/timing)

# Issues as of 09162016:
#   1) Infinite while loop in function 'find_sargassum'


def main():

    startTime = dt.now()

    # Below code allows user to input desired image. Currently, all test images (1-10) are in the ./PyIMG/imagery
    # directory. Code should eventually be changed to allow for user to direct the code towards an image somewhere
    # else.
    path = "../imagery/LS8/Test"
    n = input('Input Image Number: ')
    image = path + str(n) + '.jpg'  # Target image path
    nimage = path+ str(n) +'69.jpg'   # New image path
    im = Image.open(image)
    im.save(nimage)

    land_ho(nimage)             # Detect and blackout land
    cloud_search(nimage)        # Detect and blackout clouds
    grayscale(nimage, path, n)  # Convert image to grayscale to allow for Sargassum to stand  out more
    # find_sargassum(nimage) # Supposed to detect where Sargassum is... currently being a little bitch

    print(dt.now() - startTime) # Simple timer to see how long it takes to analyze an image


def land_ho(image): # Detects and blacks out land based on below configurations
    im = Image.open(image)
    px, py = im.size[0], im.size[1]
    rArr, gArr, bArr = np.array(im).T

    n = 6   # Setting allows for adjustments to sensitivity of search. Recommend keeping it below 10 for final product.
            # Variable also determines the area of pixels to be altered. Absolute minimum value is 2.
    x = 0
    while x < px - n:
        y = 0
        while y < py - n:
            rAvg, gAvg, bAvg = get_average_color(x, y, n, rArr, gArr, bArr)

            if rAvg > 80 or gAvg > 85:  # Blacks out area of pixels based one red and green average of the area.
                                        # Needs further tuning and testing.

                rArr, gArr, bArr = blackout(x, y, n, rArr, gArr, bArr)

            y += int(n/2)
        x += int(n/2)

    im = Image.fromarray(np.dstack([item.T for item in (rArr, gArr, bArr)]))
    im.save(image)


def cloud_search(image):    # Detects and blacks out clouds (11px x 11px) based on below configurations
    im = Image.open(image)
    px, py = im.size[0], im.size[1]
    rArr, gArr, bArr = np.array(im).T
    x = 0
    while x < px:
        y = 0
        while y < py:
            if rArr[x,y] > 100 and gArr[x,y] > 100 and bArr[x,y] > 100: # Blacks out 11px x 11px area based on
                                                                        # threshold. Should be tested with varying
                                                                        # levels to determine optimal configuration.
                rArr, gArr, bArr = blackout(x, y, 10, rArr, gArr, bArr)

            y += 1
        x += 1

    im = Image.fromarray(np.dstack([item.T for item in (rArr, gArr, bArr)]))
    im.save(image)


def find_sargassum(image):  # Finds and highlights Sargassum in a grayscale image based on below configurations
    im = Image.open(image)
    px, py = im.size[0], im.size[1]
    grayArr = np.array(im).T

    n = 2 # Variable
    x = 0
    while x < px - n:
        y = 0
        while y < py - n:
            grayAvg = get_average_gray(x, y, n, grayArr)
            if grayAvg >= 8 and grayArr[x,y] >= 10:
                grayArr = whiteout(x, y,px, py, n, grayArr)
            y += int(n / 2)
        x += int(n / 2)

    im = Image.fromarray(np.dstack([item.T for item in (grayArr)]))
    im.save(image)


def get_average_color(x, y, n, rArr, gArr, bArr):   # Determines and returns the average RGB values of an area
    r, g, b = 0, 0, 0
    i, j = x, y
    count = 0

    while i < x + n:
        while j < y + n:
            r += rArr[i, j]
            g += gArr[i, j]
            b += bArr[i, j]
            count += 1
            j += 1
        i += 1

    return int(r / count), int(g / count), int(b / count)


def get_average_gray(x, y, n, grayArr):     # Determines and returns the average values of an area in a grayscale image
    gr = 0
    i, j = x, y
    count = 0

    while i < x + n:
        while j < y + n:
            gr += grayArr[i, j]
            count += 1
            j += int(n/2)
        i += int(n/2)

    return int(gr / count)


def blackout(x, y, n, rArr, gArr, bArr):    # Converts an area of pixels in an RBG image to black

    try:
        for i in range(int(np.abs(x-n/2)), int(x+n/2)):
            for j in range(int(np.abs(y-n/2)), int(y+n/2)):
                rArr[i, j] = 0
                gArr[i, j] = 0
                bArr[i, j] = 0
    except:
        pass

    return rArr, gArr, bArr


def whiteout(x, y, px, py, n, grayArr): # Converts an area of pixels in a grayscale image to white

    for i in range(int(np.abs(x-n/2)), int(x+n/2)):
        for j in range(int(np.abs(y-n/2)), int(y+n/2)):

            grayArr[i, j] = 0

    return grayArr


def grayscale(image, path, n):  # Converts RGB image to Grayscale
    image = cv2.imread(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path + str(n) + '69.jpg', gray_image)

main()
