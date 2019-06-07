import cv2
import numpy as np

#captura = cv2.VideoCapture(0)
#kernel = np.ones((5, 5), np.uint8)

#while (True):

#    _, imagen = captura.read()
#    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

#    ret, frame = captura.read()


# Azules:
#    azul_bajos = np.array([100, 65, 75], dtype=np.uint8)
#    azul_altos = np.array([130, 255, 255], dtype=np.uint8)




 #   mascara_azul = cv2.inRange(hsv, azul_bajos, azul_altos)

#    mask = cv2.add(mascara_azul, mascara_azul)
#    mask = cv2.add(mask, mascara_azul)

#    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#    x, y, w, h = cv2.boundingRect(opening)
#    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
#    cv2.circle(frame, (int(x + w / 2), int(y + h / 2)), 6, (0, 0, 100), -1)
#    cv2.imshow('camara', frame)
#    k = cv2.waitKey(1) & 0xFF
#    if k == 27:
#        break



#from PIL import Image
#img = Image.open(".jpeg")
#img2.save("img2.jpg")

#img3 = img.crop((640,392,1200, 742))
#img3.save(".jpg")

import numpy
from PIL import Image, ImageDraw

# read image as RGB and add alpha (transparency)
im = Image.open(".jpeg").convert("RGB")

# convert to numpy (for convenience)
imArray = numpy.asarray(im)

# create mask
polygon = [
    [(1071, 547), (670, 659), (755, 1014), (1227, 857)]
]
#polygon2=[(1170, 388), (701, 390), (647, 732), (1208, 740)]

maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
for poli in polygon:
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
mask = numpy.array(maskIm)

# assemble new image (uint8: 0-255)
newImArray = numpy.empty(imArray.shape,dtype='uint8')


for f in range(len(mask)):
    for c in range(len(mask[f])):
        if mask[f][c] != 0:
            newImArray[f][c] = imArray[f][c]

# colors (three first columns, RGB)
#newImArray[:,:,:3] = imArray[:,:,:3]



# transparency (4th column)
#newImArray[:,:,3] = mask*255
# back to Image from numpy
#print("Con trasparencia")
#print(newImArray)

newIm = Image.fromarray(newImArray, "RGB")

newIm.save(".jpg")






































