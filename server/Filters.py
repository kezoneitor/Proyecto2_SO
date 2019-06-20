from builtins import print
import numpy as np
import cv2
import datetime
from  threading import Thread
import time
import queue
import multiprocessing
from Connection import *

q = queue.Queue()
CANNY = 250
MORPH = 10
_width = 1920.0
_height = 1080.0
_margin = 0.0
lower_range = np.array([81, 25, 144])
upper_range = np.array([130, 255, 255])
area = 5000

#Validar que sea un numero
def isNumber(num):
    try:
        int(num)
        return True
    except:
        return False

def worker():
    global q
    while True:
        item = q.get()
        print("en proceso...")
        dir = item[2] + str(item[1]) + "_" + item[3]
        cv2.imwrite(dir + ".jpeg", item[0])
        save = reconocer_panel(item[0])
        if save:
            writeImage(item[2], str(item[1]) + "_" + item[3] + ".jpeg")
        q.task_done()

#Crear las imagenes en la base de datos
def ejecutarCrearImagenesV2(nombre_archivo, nombre_carpeta, cantFrames):
    if(isNumber(cantFrames) and nombre_archivo != "File name"):
        global q
        #Información de los videos y cantidad de frames
        nombre = str(datetime.datetime.now()) + nombre_archivo.split('\\')[len(nombre_archivo.split('\\')) - 1]
        nombre = nombre[0:len(nombre) - 4].replace(".", "_").replace(":", "_")
        nombre_carpeta = nombre_carpeta.replace("\\", "/") + "/"
        numFrames = int(cantFrames)
        img_process = cv2.imread("./en_proceso.png")
        #Video a capturar y calcular frames
        video = cv2.VideoCapture(nombre_archivo)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        fr = (fps // numFrames)
        i = 0
        see_video = False
        # variables para el reconocimiento de formas

        #Ejecución de los hilos con respecto a la cantidad de nucleos de la pc
        cpus = multiprocessing.cpu_count()  # detect number of cores
        for i in range(cpus):
            t = Thread(target=worker)
            t.start()
        start_time = time.time()
        while (True):
            cv2.imshow("En proceso", img_process)
            # Capture frame-by-frame
            ret, frame = video.read()
            #Cambiar dimensiones de la imagen
            img = cv2.resize(frame, (int(_width), int(_height)))

            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('c') or not(ret):
                break
            elif cv2.waitKey(20) & 0xFF == ord('v'):
                see_video = True
            if see_video:
                cv2.imshow("nombre", img)

            if (i % (int(fps / numFrames)) == 0):
                data = [img, i, nombre_carpeta, nombre]
                q.put(data)
            i += 1
        q.join()  # block until all tasks are done
        print("--- %s seconds ---" % (time.time() - start_time))
        # When everything done, release the capture
        video.release()
        cv2.destroyAllWindows()
        return "Proceso terminado"
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"

def reconocer_panel(img):
    global CANNY
    global MORPH
    global _width
    global _height
    global _margin
    global lower_range
    global upper_range
    global area
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
            if (len(approx) == 4):
                return True
            else: pass
        else: pass


