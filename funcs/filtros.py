import numpy as np
import imageio
import cv2
import datetime
from  threading import Thread
from database.conexion import *

#Validar que sea un numero
def isNumber(num):
    try:
        int(num)
        return True
    except:
        return False

#Crear las imagenes en la base de datos
def ejecutarCrearImagenes(nombre_archivo, cantFrames):
    if(isNumber(cantFrames) and nombre_archivo != "File name"):
        numFrames = int(cantFrames)
        video = cv2.VideoCapture(nombre_archivo)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        nombre = str(datetime.datetime.now())+nombre_archivo.split('\\')[len(nombre_archivo.split('\\'))-1]
        i=0
        listaProcesos = []
        while (True):
            # Capture frame-by-frame
            ret, frame = video.read()
            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
            """
            elif not(ret):
                for p in listaProcesos:
                    p.start()
                for p in listaProcesos:
                    p.join()
                break
            
            cv2.imshow("Process video: " + nombre, frame)
            if (i % (int(fps / numFrames)) == 0):
                cv2.imshow("Process video: " + nombre, frame)
                proceso = Thread(target=writeImage, args=(frame, str(i) + "?" + nombre))
                listaProcesos.append(proceso)
            i += 1
            """
            calcular_imagen(frame, 127)

        # When everything done, release the capture
        video.release()
        cv2.destroyAllWindows()
    else:
        return "Inserte un número en el campo: 'Tomar___fps' y eliga un archivo"
    return "Proceso Ejecutado con exito"

#filtro para hacer nitidez a la imagen
def nitidez(img):
    # Create our shapening kernel, it must equal to one eventually
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    # applying the sharpening kernel to the input image & displaying it.
    sharpened = cv2.filter2D(img, -1, kernel_sharpening)
    return sharpened
"""
#para calcular si es muy clara o oscura la imagen
def calcular_imagen(frame, thrshld):
    #imagen_f = imageio.read(filename, as_gray=True)
    is_light = np.mean(frame) > thrshld
    if is_light:
        return oscurecer(frame, 0.6)
    else:
        return aclarar(frame,30)

#filtro de aclarar
def aclarar(img,increase):
    a = np.double(img)
    b = a + increase
    img2 = np.uint8(b)
    cv2.imshow('Lightess', img2)
    return img2

#filtro para oscurecer la imagen
def oscurecer(img,valor):
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsvImg[..., 2] = hsvImg[..., 2] * valor
    image = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
    cv2.imshow('Darkness', image)
    return image
"""


ejecutarCrearImagenes("C:/Users/Kezo/Documents/GitProjects/Project2_SO_VKP/Proyecto2_SO/funcs/data/orig_14.jpg",30)