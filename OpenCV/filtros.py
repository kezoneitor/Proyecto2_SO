import cv2
import numpy as np
import imageio

#variable de nombre de archivo
nombre_archivo ="./data/second_0.jpg"

# Reading in and displaying our image
image = cv2.imread(nombre_archivo)
cv2.imshow('Original', image)

#filtro para hacer nitidez a la imagen
def nitidez(img):
    # Create our shapening kernel, it must equal to one eventually
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    # applying the sharpening kernel to the input image & displaying it.
    sharpened = cv2.filter2D(img, -1, kernel_sharpening)
    cv2.imshow('Imagen nitida', sharpened)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#filtro para oscurecer la imagen
def oscurecer(img,valor):

    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsvImg[..., 2] = hsvImg[..., 2] * valor

    image = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)

    cv2.imshow('Darkness', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#calcular_imagen(nombre_archivo,127)
# aclarar(image,30)
oscurecer(image, 0.6)
#nitidez(image)

