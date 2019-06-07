import cv2
import numpy as np



# Read the picure - The 1 means we want the image in BGR

CANNY = 250
MORPH = 10
_width  = 720.0
_height = 480.0
_margin = 0.0
area = 500

def nothing(x):
    # any operation
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L-S", "Trackbars", 12, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 47, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 79, 255, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("AREA", "Trackbars", 40, 10000, nothing)


# wait to user to press [ ESC ]
while (True):
    img = cv2.imread('.jpeg')
    # resize img to 20% in each axis
    #img = cv2.resize(img, (560, 350))
    # convert BGR image to a HSV image
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    area = cv2.getTrackbarPos("AREA", "Trackbars")

    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # NumPy to create arrays to hold lower and upper range
    # The “dtype = np.uint8” means that data type is an 8 bit integer
    #lower_range = np.array([60, 35, 72], dtype=np.uint8)
    #upper_range = np.array([130, 255, 255], dtype=np.uint8)

    # create a mask for image
    mask = cv2.inRange(hsv, lower_range, upper_range)
    corners = np.array(
        [
            [[  	_margin, _margin 			]],
            [[ 			_margin, _height + _margin  ]],
            [[ _width + _margin, _height + _margin  ]],
            [[ _width +_margin, _margin 			]],
        ]
    )
    pts_dst = np.array(corners, np.float32)

    gray = cv2.bilateralFilter(mask, 1, 10, 120)

    edges = cv2.Canny(gray, 10, CANNY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))

    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, h = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:

        # Küçük alanları pass geç
        if cv2.contourArea(cont) > area:

            arc_len = cv2.arcLength(cont, True)

            approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)
                #if (len(approx) == 4):
            IS_FOUND = 1
            M = cv2.moments(cont)
            #cX = int(M["m10"] / M["m00"])
            #cY = int(M["m01"] / M["m00"])
            #cv2.putText(img, "Panel Solar", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            pts_src = np.array(approx, np.float32)

            #h, status = cv2.findHomography(pts_src, pts_dst)
            #out = cv2.warpPerspective(img, h, (int(_width + _margin * 2), int(_height + _margin * 2)))

            cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)

            #else: pass

    cv2.imshow('edges', edges)
    cv2.imshow('rgb', img)
    # cv2.circle(img, (int(x + w / 2), int(y + h / 2)), 6, (0, 0, 100), -1)
    # display both the mask and the image side-by-side
    cv2.imshow('mask', mask)
    # cv2.imshow('image', img)
    if (cv2.waitKey(27) & 0xFF == ord('q')):
        break

cv2.destroyAllWindows()