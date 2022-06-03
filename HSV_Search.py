import cv2 as cv

def nothing(x):
    pass

cap = cv.VideoCapture("kursach.test4.mp4")

cv.namedWindow('result')

cv.createTrackbar('minb', 'result', 0, 255, nothing)
cv.createTrackbar('ming', 'result', 0, 255, nothing)
cv.createTrackbar('minc', 'result', 0, 255, nothing)

cv.createTrackbar('maxb', 'result', 0, 255, nothing)
cv.createTrackbar('maxg', 'result', 0, 255, nothing)
cv.createTrackbar('maxc', 'result', 0, 255, nothing)

#color = cv.imread("Color.png")

while(True):

    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    cv.imshow("hsv", hsv)

    minb = cv.getTrackbarPos('minb', 'result')
    ming = cv.getTrackbarPos('ming', 'result')
    minc = cv.getTrackbarPos('minc', 'result')

    maxb = cv.getTrackbarPos('maxb', 'result')
    maxg = cv.getTrackbarPos('maxg', 'result')
    maxc = cv.getTrackbarPos('maxc', 'result')

    hsv = cv.blur(hsv, (5,5))
    cv.imshow("blur", hsv)

    mask = cv.inRange(hsv, (minb, ming, minc), (maxb, maxg, maxc))
    cv.imshow('mask', mask)

   # mask2 = cv.inRange(color,(minb, ming, minc), (maxb, maxg, maxc))
   # cv.imshow('mask2', mask2)

    # Убираем белые отдельно стоящие пиксели
    maskEr = cv.erode(mask, None, iterations=2)
    cv.imshow("Erode", maskEr)

    # Увиличиваем большие белые объекты, вместе с erode мы получаем более чистую картинку
    maskDi = cv.dilate(maskEr, None, iterations=2)
    cv.imshow("Dilate", maskDi)

    result = cv.bitwise_and(frame, frame, mask = mask)
    cv.imshow('result', result)

   # result2 = cv.betwise_and(color, color, mask = mask)
   # cv.imshow('result2', result)

    if cv.waitKey(1) == ord('w'):
        break

        cap.release()
        cv.destroyAllWindows()