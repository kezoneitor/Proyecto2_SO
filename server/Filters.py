import numpy as np
import cv2
import datetime
from  threading import Thread
from server.Connection import *

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
        while (True):
            # Capture frame-by-frame
            ret, frame = video.read()
            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
            elif not(ret):
                for p in listaProcesos:
                    p.start()
                for p in listaProcesos:
                    p.join()
                break
            
            if (i % (int(fps / numFrames)) == 0):
                cv2.imshow("Process video: " + nombre, frame)
                cv2.imwrite(nombre_carpeta+str(i)+"_"+nombre+".jpg", frame)
                proceso = Thread(target=writeImage, args=(nombre_carpeta, str(i)+"_"+nombre+".jpg"))
                listaProcesos.append(proceso)
            else:
                cv2.imshow("Process video: " + nombre, frame)
            i += 1

        # When everything done, release the capture
        video.release()
        cv2.destroyAllWindows()
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"
    return "Proceso Ejecutado con exito"


#Crear funcion que ejecute "generar_Imagenes(nombre_carpeta, inicio, final)" en el cliente