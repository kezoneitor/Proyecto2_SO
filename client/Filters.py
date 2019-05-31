import numpy as np
import cv2
import multiprocessing
from  threading import Thread
import queue
from client.Connection import *

q = queue.Queue()


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

def aplicar_Filtros(path):
    img = cv2.imread(path[0]+path[1])
    nit = nitidez(img)
    lap = lapician(nit)
    cv2.imwrite(path[0]+path[1], lap)
    updateImage(path)

def generar_Imagenes(nombre_carpeta, inicio, final):
    arr_img = readImage(nombre_carpeta, inicio, final)
    for path in arr_img:
        q.put(path)
    cpus = multiprocessing.cpu_count()  # detect number of cores
    print("Creating %d threads" % cpus)
    for i in range(cpus):
        t = multiprocessing.Process(target=worker)
        t.daemon = True
        t.start()

def worker():
    global q
    while True:
        item = q.get()
        img = cv2.imread(item[0] + item[1])
        nit = nitidez(img)
        lap = lapician(nit)
        cv2.imwrite(item[0] + item[1], lap)
        updateImage(item)
        q.task_done()