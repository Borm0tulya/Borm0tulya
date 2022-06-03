import numpy as np
import cv2 as cv

cap = cv.VideoCapture("kursach.test.mp4")

while (True):
    ret, frame  = cap.read ()
    cv.imshow("Vidos", frame)

    print(frame)

    mask = cv.inRange(frame, (100,100,100),(255,255,255))
    cv.imshow("Mask", mask)

    if cv.waitKey(1)  == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
