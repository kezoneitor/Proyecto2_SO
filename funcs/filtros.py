import numpy as np
import imageio
import cv2
import datetime
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
        while (True):
            # Capture frame-by-frame
            ret, frame = video.read()
            # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
            if cv2.waitKey(20) & 0xFF == ord('q') or not(ret):
                break
            if(i%(int(fps/numFrames)) == 0):
                x = cv2.circle(frame, (30, 30), 30, (0, 0, 255), -1)
                cv2.imshow("Process video: " + nombre, x)
                writeImage(frame, str(i)+"?"+nombre)
            else:
                cv2.imshow("Process video: " + nombre, frame)
            i += 1

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

#para calcular si es muy clara o oscura la imagen
def calcular_imagen(filename, thrshld):
    imagen_f = imageio.imread(filename, as_gray=True)
    is_light = np.mean(imagen_f) > thrshld
    if is_light:
        print("light")
    else:
        print("dark")

#filtro de aclarar
def aclarar(img,increase):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = image[:, :, 2]
    v = np.where(v <= 255 - increase, v + increase, 255)
    image[:, :, 2] = v
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imshow('Brightness', image)

#filtro para oscurecer la imagen
def oscurecer(img,valor):
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsvImg[..., 2] = hsvImg[..., 2] * valor
    image = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
    cv2.imshow('Darkness', image)