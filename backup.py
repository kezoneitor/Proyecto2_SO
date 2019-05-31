import numpy as np
import cv2
import datetime
from  threading import Thread
from server.Connection import *
import time

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
        listaProcesos = []
        start_time = time.time()
        while (True):
            # Capture frame-by-frame
            ret, frame = video.read()
            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('q') or not(ret):

                for p in listaProcesos:
                    p.start()
                for p in listaProcesos:
                    p.join()
                break
            if (i % (int(fps / numFrames)) == 0):
                #cv2.imshow("Process video: " + nombre, frame)
                cv2.imwrite(nombre_carpeta+str(i)+"_"+nombre+".jpg", frame)
                writeImage(nombre_carpeta, str(i)+"_"+nombre+".jpg")
                proceso = Thread(target=writeImage, args=(nombre_carpeta, str(i)+"_"+nombre+".jpg"))
                proceso.daemon = True
                listaProcesos.append(proceso)
            #else:
                #cv2.imshow("Process video: " + nombre, frame)
            i += 1

        # When everything done, release the capture
        print("--- %s seconds ---" % (time.time() - start_time))
        video.release()
        cv2.destroyAllWindows()
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"
    return "Proceso Ejecutado con exito"

#Crear las imagenes en la base de datos
def ejecutarCrearImagenesV2(nombre_archivo, nombre_carpeta, cantFrames):
    if(isNumber(cantFrames) and nombre_archivo != "File name"):
        nombre = str(datetime.datetime.now()) + nombre_archivo.split('\\')[len(nombre_archivo.split('\\')) - 1]
        nombre = nombre[0:len(nombre) - 4].replace(".", "_").replace(":", "_")
        nombre_carpeta = nombre_carpeta.replace("\\", "/") + "/"
        numFrames = int(cantFrames)

        video = cv2.VideoCapture(nombre_archivo)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        lista_procesos = []
        fr = (fps // numFrames)
        i = fr
        start_time = time.time()
        while i < total_frames:
            # Capture frame-by-frame
            print("Proceso", (i // total_frames) * 100, "%")
            procesoPrincipal(video, i, nombre_carpeta, str(i)+"_"+nombre+".jpg")
            proceso = Thread(target=procesoPrincipal, args=(video, i, nombre_carpeta, str(i)+"_"+nombre+".jpg",))
            lista_procesos.append(proceso)
            i += fr
        print("--- %s seconds ---" % (time.time() - start_time))
        # When everything done, release the capture
        video.release()
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"
    return "Proceso Ejecutado con exito"

def procesoPrincipal(video, i, nombre_carpeta, nombre):
    video.set(1, (i - 1))
    ret, frame = video.read()
    cv2.imwrite(nombre_carpeta + str(i) + "_" + nombre + ".jpg", frame)
    writeImage(nombre_carpeta, str(i) + "_" + nombre + ".jpg")

#Crear funcion que ejecute "generar_Imagenes(nombre_carpeta, inicio, final)" en el cliente