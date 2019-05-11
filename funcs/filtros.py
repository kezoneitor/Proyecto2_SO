import cv2
import numpy as np
import imageio

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

#calcular_imagen(nombre_archivo,127)
# aclarar(image,30)
#oscurecer(image, 0.6)
#nitidez(image)

def ejecutarCrearImagenes(nombre_archivo, guardar_en, cantFrames, videoFps):
    video = cv2.VideoCapture(nombre_archivo)
    print(video)
    i=0
    while (True):
        # Capture frame-by-frame
        ret, frame = video.read()
        # Condiciones de salida >> Presionar la letra 'q' o que ya no existen mas frames
        if cv2.waitKey(20) & 0xFF == ord('q') or not(ret):
            break
        cv2.imshow('frame',frame)
        if(i%(int(videoFps/cantFrames)) == 0):
            cv2.imwrite(guardar_en+'/second_'+str(i)+'.jpg',frame)
        i+=1
    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
ejecutarCrearImagenes("tkwWilliam.mp4", "data", 2, 30)