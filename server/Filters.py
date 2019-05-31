import numpy as np
import cv2
import datetime
from  threading import Thread
from server.Connection import *
import time
import queue
import multiprocessing

q = queue.Queue()
#Validar que sea un numero
def isNumber(num):
    try:
        int(num)
        return True
    except:
        return False

#Crear las imagenes en la base de datos
def ejecutarCrearImagenes(nombre_archivo, nombre_carpeta, cantFrames):
    if(isNumber(cantFrames) and nombre_archivo != "File name"):
        numFrames = int(cantFrames)
        video = cv2.VideoCapture(nombre_archivo)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        nombre = str(datetime.datetime.now())+nombre_archivo.split('\\')[len(nombre_archivo.split('\\'))-1]
        nombre = nombre[0:len(nombre)-4].replace(".","_").replace(":", "_")
        nombre_carpeta = nombre_carpeta.replace("\\", "/")+"/"
        i=0
        start_time = time.time()
        while (True):
            # Capture frame-by-frame
            ret, frame = video.read()
            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('q') or not(ret):
                break
            resizeframe = cv2.resize(frame, (720, 480))
            if (i % (int(fps / numFrames)) == 0):
                cv2.imshow("Process video: " + nombre, resizeframe)
                cv2.imwrite(nombre_carpeta+str(i)+"_"+nombre+".jpg", frame)
                writeImage(nombre_carpeta, str(i)+"_"+nombre+".jpg")
            else:
                cv2.imshow("Process video: " + nombre, resizeframe)
            i += 1

        # When everything done, release the capture
        print("--- %s seconds ---" % (time.time() - start_time))
        video.release()
        cv2.destroyAllWindows()
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"
    return "Proceso Ejecutado con exito"

def worker():
    global q
    while True:
        item = q.get()
        cv2.imwrite(item[2] + str(item[1]) + "_" + item[3] + ".jpg", item[0])
        writeImage(item[2], str(item[1]) + "_" + item[3] + ".jpg")
        q.task_done()

#Crear las imagenes en la base de datos
def ejecutarCrearImagenesV2(nombre_archivo, nombre_carpeta, cantFrames):
    if(isNumber(cantFrames) and nombre_archivo != "File name"):
        global breaki
        nombre = str(datetime.datetime.now()) + nombre_archivo.split('\\')[len(nombre_archivo.split('\\')) - 1]
        nombre = nombre[0:len(nombre) - 4].replace(".", "_").replace(":", "_")
        nombre_carpeta = nombre_carpeta.replace("\\", "/") + "/"
        numFrames = int(cantFrames)

        video = cv2.VideoCapture(nombre_archivo)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        #total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fr = (fps // numFrames)
        i = fr
        start_time = time.time()
        while (True):
            # Capture frame-by-frame
            ret, frame = video.read()
            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('q') or not(ret):
                break
            if (i % (int(fps / numFrames)) == 0):
                cv2.imshow("Process video: " + nombre, frame)
                data = [frame, i, nombre_carpeta, str(i) + "_" + nombre + ".jpg"]
                q.put(data)
            else:
                cv2.imshow("Process video: " + nombre, frame)
            i += 1
        q.join() # block until all tasks are done
        print("--- %s seconds ---" % (time.time() - start_time))
        # When everything done, release the capture
        video.release()
        cv2.destroyAllWindows()

        return "Proceso terminado"
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"
#Crear funcion que ejecute "generar_Imagenes(nombre_carpeta, inicio, final)" en el cliente