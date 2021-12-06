import sys
from PIL import Image
from tkinter import *
from PIL import ImageTk, Image
from PIL.ImageOps import pad, crop

im = ""
imCopy = ""
isRgb = True
isHelp = True


def helpCheck():
    for x in range(len(sys.argv)):
        if x == len(sys.argv) - 1:
            im_path = sys.argv[x]
    if not im_path == "--help":
        global isHelp
        isHelp = False
    else:
        showHelp()


def initImage():
    for x in range(len(sys.argv)):
        if x == len(sys.argv) - 1:
            im_path = sys.argv[x]
    global im
    global imCopy
    global isRgb
    im = Image.open(str(im_path))
    imCopy = im.copy()
    #  greyscale check
    if isinstance(imCopy.getpixel((0, 0)), int):
        isRgb = False
    else:
        imCopy.convert('RGB')

# arguments: brightness[0;0.1;10], threshold[0;255], contrast[-255;255],
# blur[1,2], sharpen, changeColor[12,13,23], erode, dilate


def runArguments():
    for x in range(len(sys.argv)):
        firstLetters = sys.argv[x][:4]
        if x + 1 < len(sys.argv):
            if not any(z.isalpha() for z in sys.argv[x + 1]):
                callFunction(firstLetters, sys.argv[x + 1])
            else:
                callFunction(firstLetters, str(0))


def callFunction(name, value):
    if name == "--br":
        brightness(float(value))
        showTk(imCopy)
    if name == "--th":
        threshold(int(value))
        showTk(imCopy)
    if name == "--co":
        contrast(int(value))
        showTk(imCopy)
    if name == "--bl":
        blur(imCopy, int(value))
        showTk(imCopy)
    if name == "--sh":
        sharpen(imCopy)
        showTk(imCopy)
    if name == "--ch":
        if int(value) == 12:
            changeColorChannel(0, 1)
        if int(value) == 13:
            changeColorChannel(0, 2)
        if int(value) == 23:
            changeColorChannel(1, 2)
        showTk(imCopy)
    if name == "--er":
        erode(imCopy)
        showTk(imCopy)
    if name == "--di":
        dilate(imCopy)
        showTk(imCopy)


def showHelp():
    helpText = "\nWelcome at Mini-Gimp!\nThe following methods are availabe:\n\n\
        --brightness (--br) followed by a float which multiplies the brightness -->                     --br 0.2\n\
        --threshold (--th) followed by a int [0;255] with 255 turning the picture complete dark -->     --th 200\n\
        --contrast (--co) followed by a int [-255;255] with 255 making the most contrast -->            --co -100\n\
        --blur (--bl) followed by a int either 1 or 2 which changes the kernel -->                      --bl 2\n\
        --sharpen (--sh) -->                                                                            --sh\n\
        --changeColorChannel (--ch) followed by 12, 13 or 23 which represents the changing channels --> --ch 13\n\
        --erode (--er) -->                                                                              --er\n\
        --dilate (--di) -->                                                                             --di\n\n\
        Example Input: python3 minigimp.py --br 0.4 --th 200 --er picture.jpg"
    print(helpText)

# show Image in Tk


def showTk(image):
    root = Tk()
    imgTk = ImageTk.PhotoImage(image)
    panel = Label(root, image=imgTk)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


# helper function prints every 2000' pixel
def printPixel():
    num = 0
    for x in range(imCopy.width):
        for y in range(imCopy.height):
            num += 1
            if num % 2000 == 0:
                print(imCopy.getpixel((x, y)))
    print("----------DONE----------")


# value [0;10] times as bright
def brightness(value):
    #  RGB pic
    if(isRgb):
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                pixellist = list(pixel)
                for z in range(3):
                    pixellist[z] = int(pixellist[z] * value)
                    if pixellist[z] > 255:
                        pixellist[z] = 255
                pixel = tuple(pixellist)
                imCopy.putpixel((x, y), pixel)
    # greyscale pic
    else:
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                if pixel > 255:
                    pixel = 255
                else:
                    pixel = pixel * value
                    imCopy.putpixel((x, y), int(pixel))


# value [0;255] 255 = complete dark pic
def threshold(value):
    #  RGB pic
    if(isRgb):
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                pixellist = list(pixel)
                for z in range(3):
                    if pixellist[z] < value:
                        pixellist[z] = 0
                    else:
                        pixellist[z] = 255
                pixel = tuple(pixellist)
                imCopy.putpixel((x, y), pixel)
    # greyscale pic
    else:
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                if pixel < value:
                    pixel = 0
                else:
                    pixel = 255
                imCopy.putpixel((x, y), pixel)


# value [-255;255]
def contrast(value):
    factor = (259 * (value + 255)) / (255 * (259 - value))
    #  RGB pic
    if(isRgb):
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                pixellist = list(pixel)
                for z in range(3):
                    pixellist[z] = int(factor * (pixellist[z] - 128) + 128)
                    if pixellist[z] > 255:
                        pixellist[z] = 255
                pixel = tuple(pixellist)
                imCopy.putpixel((x, y), pixel)
    # greyscale pic
    else:
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                pixel = int(factor * (pixel - 128) + 128)
                if pixel > 255:
                    pixel = 255
                imCopy.putpixel((x, y), pixel)


# apply kernel on image for blur, sharpen etc.
def applyKernel(kernel, image):
    w, h = image.size
    div = (sum(kernel[0]) + sum(kernel[1]) + sum(kernel[2]))
    img = pad(image, (w + 2, h + 2))

    # RGB pic
    if(isRgb):
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                pixel = (0, 0, 0)
                pixellist = list(pixel)
                for i in range(3):
                    for j in range(3):
                        for z in range(3):
                            pixellist[z] += int(image.getpixel((x - 1 + i, y - 1 + j))[
                                                z] * kernel[i][j] / (div + 0.01))
                pixel = tuple(pixellist)
                img.putpixel((x, y), pixel)
    # greyscale
    else:
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                pixel = 0
                for i in range(3):
                    for j in range(3):
                        pixel += int(image.getpixel((x - 1 + i, y - 1 + j))
                                     * kernel[i][j] / (div + 0.01))
                img.putpixel((x, y), pixel)
    image = crop(img, 1)
    global imCopy
    imCopy = image


def blur(image, value):
    if value == 1:
        kernel = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    if value == 2:
        kernel = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    applyKernel(kernel, image)


def sharpen(image):
    kernel = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
    applyKernel(kernel, image)


def changeColorChannel(num1, num2):
    if(isRgb):
        for x in range(imCopy.width):
            for y in range(imCopy.height):
                pixel = imCopy.getpixel((x, y))
                pixellist = list(pixel)
                colorValue = pixellist[num1]
                pixellist[num1] = pixellist[num2]
                pixellist[num2] = colorValue
                pixel = tuple(pixellist)
                imCopy.putpixel((x, y), pixel)


def erode(image):
    w, h = image.size
    img = pad(image, (w + 2, h + 2))

    # RGB pic
    if(isRgb):
        # process each color channel independently
        for z in range(3):
            for x in range(1, w - 1):
                for y in range(1, h - 1):
                    min = 256
                    for i in range(3):
                        for j in range(3):
                            pixel = image.getpixel((x - 1 + i, y - 1 + j))
                            pixellist = list(pixel)
                            if pixellist[z] < min:
                                min = pixellist[z]
                    pixel2 = image.getpixel((x, y))
                    pixellist2 = list(pixel2)
                    pixellist2[z] = min
                    pixel2 = tuple(pixellist2)
                    img.putpixel((x, y), pixel2)
        # overwrite image after every color channel to not only erode over the
        # last channel
        image = crop(img, 1)
    # greyscale
    else:
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                min = 256
                for i in range(3):
                    for j in range(3):
                        pixel = image.getpixel((x - 1 + i, y - 1 + j))
                        if pixel < min:
                            min = pixel
                img.putpixel((x, y), min)
    image = crop(img, 1)
    global imCopy
    imCopy = image


def dilate(image):
    w, h = image.size
    img = pad(image, (w + 2, h + 2))

    # RGB pic
    if(isRgb):
        for z in range(3):
            for x in range(1, w - 1):
                for y in range(1, h - 1):
                    max = 0
                    for i in range(3):
                        for j in range(3):
                            pixel = image.getpixel((x - 1 + i, y - 1 + j))
                            pixellist = list(pixel)
                            if pixellist[z] > max:
                                max = pixellist[z]
                    pixel2 = image.getpixel((x, y))
                    pixellist2 = list(pixel2)
                    pixellist2[z] = max
                    pixel2 = tuple(pixellist2)
                    img.putpixel((x, y), pixel2)
        image = crop(img, 1)
    # greyscale
    else:
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                max = 0
                for i in range(3):
                    for j in range(3):
                        pixel = image.getpixel((x - 1 + i, y - 1 + j))
                        if pixel > max:
                            max = pixel
                img.putpixel((x, y), max)
    image = crop(img, 1)
    global imCopy
    imCopy = image


def runCode():
    helpCheck()
    if not isHelp:
        initImage()
        showTk(imCopy)
        runArguments()


runCode()
