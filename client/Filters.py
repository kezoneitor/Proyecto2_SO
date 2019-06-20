import numpy as np
import cv2
import multiprocessing
from  threading import Thread
import queue
from Connection import *
import time
from PIL import Image, ImageDraw

q = queue.Queue()
CANNY = 250
MORPH = 10
_width = 1920.0
_height = 1080.0
_margin = 0.0

"""
#filtro para hacer nitidez a la imagen
def nitidez(img):
    # Create our shapening kernel, it must equal to one eventually
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    # applying the sharpening kernel to the input image & displaying it.
    sharpened = cv2.filter2D(img, -1, kernel_sharpening)
    return sharpened

def lapician(img):
    lap = cv2.Laplacian(img,cv2.CV_64F)
    return lap
"""

def generar_Imagenes(nombre_carpeta, inicio, final):
    arr_img = readImage(nombre_carpeta, inicio, final)
    cpus = multiprocessing.cpu_count()  # detect number of cores
    print("Creating %d threads" % cpus)
    for i in range(cpus):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    start_time = time.time()
    for path in arr_img:
        q.put(path)
    q.join()
    print("--- %s seconds ---" % (time.time() - start_time))

def worker():
    global q
    while True:
        item = q.get()
        recortar_panel(item[0] + item[1], np.array([81, 25, 144]), np.array([130, 255, 255]), 5000)
        save = reconocer_basura(item[0] + item[1], np.array([0, 12, 47]), np.array([50, 255, 255]), 45)
        if not(save):
            print("se borro", item[1])
            delete_db(item[1])
        print("se mantuvo", item[1])
        q.task_done()

def recortar_panel(name_dir, lower_range, upper_range, area):
    global CANNY
    global MORPH
    global _width
    global _height
    global _margin
    img = cv2.imread(name_dir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # NumPy to create arrays to hold lower and upper range
    # The “dtype = np.uint8” means that data type is an 8 bit integer

    # create a mask for image
    mask = cv2.inRange(hsv, lower_range, upper_range)

    gray = cv2.bilateralFilter(mask, 1, 10, 120)

    edges = cv2.Canny(gray, 10, CANNY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))

    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, h = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    list_polygon = []
    x = []
    y = []
    for cont in contours:

        if cv2.contourArea(cont) > area:
            arc_len = cv2.arcLength(cont, True)

            approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)

            if (len(approx) == 4):
                l1 = (approx[0][0][0], approx[0][0][1])
                l2 = (approx[1][0][0], approx[1][0][1])
                l3 = (approx[2][0][0], approx[2][0][1])
                l4 = (approx[3][0][0], approx[3][0][1])
                polygon = [l1, l2, l3, l4]
                x += [l1[0], l2[0], l3[0], l4[0]]
                y += [l1[1], l2[1], l3[1], l4[1]]
                list_polygon.append(polygon)

            else: pass
    if (len(x) != 0 and len(y) != 0):
        im = Image.open(name_dir).convert("RGB")
        # convert to numpy (for convenience)
        imArray = np.asarray(im)

        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        for p in list_polygon:
            ImageDraw.Draw(maskIm).polygon(p, outline=1, fill=1)
        mask_fig = np.array(maskIm)
        # assemble new image (uint8: 0-255)
        newImArray = np.empty(imArray.shape, dtype='uint8')

        for f in range(len(mask_fig)):
            for c in range(len(mask_fig[f])):
                if mask_fig[f][c] != 0:
                    newImArray[f][c] = imArray[f][c]

        # back to Image from numpy
        newIm = Image.fromarray(newImArray, "RGB")

        cut_pL = [min(x), min(y)]
        cut_pH = [max(x), max(y)]

        justIm = newIm.crop((cut_pL[0],cut_pL[1],cut_pH[0], cut_pH[1]))
        justIm.save(name_dir)

def reconocer_basura(name_dir, lower_range, upper_range, area):
    global CANNY
    global MORPH
    global _width
    global _height
    global _margin
    img = cv2.imread(name_dir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # NumPy to create arrays to hold lower and upper range
    # The “dtype = np.uint8” means that data type is an 8 bit integer

    # create a mask for image
    mask = cv2.inRange(hsv, lower_range, upper_range)

    gray = cv2.bilateralFilter(mask, 1, 10, 120)

    edges = cv2.Canny(gray, 10, CANNY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))

    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, h = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:

        if cv2.contourArea(cont) > area:
            arc_len = cv2.arcLength(cont, True)

            approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)
            if len(approx) != 0:
                return True
    return False