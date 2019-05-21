import numpy as np
import cv2
import datetime
from  threading import Thread
from client.Connection import *

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
    listaProcesos = []
    for path in arr_img:
        proceso = Thread(target=aplicar_Filtros, args=(path,))
        listaProcesos.append(proceso)
    for p in listaProcesos:
        p.start()
    for p in listaProcesos:
        p.join()