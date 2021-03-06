import numpy as np
import cv2 as cv # импорт библиотеки

cap = cv.VideoCapture("kursach.test4.mp4") #подгружаем видео
frameCounter: int = 0
while (True):
    ret, frame  = cap.read () #показываем видео
    try:
        frame = cv.resize(frame, (700, 360))
    except:
        break
    try:
        half = frame[:180, 10:2000]
    except:
        break
    #cv.imshow("half", half)
    cv.imshow("Vidos", frame)

    frameCopy = frame.copy() #создаем копию

    frame_hsv = cv.cvtColor(half, cv.COLOR_BGR2HSV)
    hsv = cv.blur(frame_hsv, (5, 5))  # блюрим
    #cv.imshow("hsv", hsv)


    # красный цвет представляет из себя две области в пространстве HSV
    lower_red = np.array([40, 50, 136], dtype="uint8")
    upper_red = np.array([182, 52, 80], dtype="uint8")

    # красный в диапазоне фиолетового оттенка
    lower_violet = np.array([140, 85, 110], dtype="uint8")
    upper_violet = np.array([180, 255, 255], dtype="uint8")

    red_mask_orange = cv.inRange(hsv, lower_red, upper_red)  # применяем маску по цвету
    red_mask_violet = cv.inRange(hsv, lower_violet, upper_violet)  # для красного таких 2

    red_mask_full = red_mask_orange + red_mask_violet  # полная масква предствавляет из себя сумму
    red_mask_full = cv.dilate(red_mask_full, None,iterations=2)  # добавляем увиличивем количество белых пикселей для четкости изображения
    cutedFrame = red_mask_full[70:200, 70:665]
    #cv.imshow("red", red_mask_full)

    # с зеленым все проще - он в центре диапазона
    lower_green = np.array([25,189,118], dtype="uint8")
    upper_green = np.array([85,255,255], dtype="uint8")


    green_mask = cv.inRange(hsv, lower_green, upper_green)
    cutedFrame1 = green_mask[70:200, 70:665]
    green_mask = cv.dilate(green_mask, None, iterations=5)  # добавляем увиличивем количество белых пикселей для четкости изображения
    green_mask = cv.erode(green_mask, None, iterations=2)  # добавляем увиличивем количество белых пикселей для четкости изображения
    #cv.imshow("green", green_mask)

    # желтый тоже достаточно просто
    lower_yellow = np.array([0, 208, 186], dtype="uint8")
    upper_yellow = np.array([47, 255, 255], dtype="uint8")
    yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    cutedFrame2 = yellow_mask[70:200, 70:665]
    #cv.imshow("yellow", yellow_mask)

    # применяем маску
    full_mask = yellow_mask + green_mask + red_mask_full
    full_mask = cv.dilate(full_mask, None, iterations=2)  # добавляем увиличивем количество белых пикселей для четкости изображения
    cutedFrame3 = full_mask[70:200, 70:665]
    #cv.imshow("full", full_mask)

    contours = cv.findContours(full_mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)  # ищем контуры
    contours = contours[0]  # оставляем только инфу о контурах
    if contours:
        cv.drawContours(frameCopy, contours, 0, (255, 255, 255), 1)  # выводим контуры на видео
        #cv.imshow("Contours", frameCopy)
        cv.imwrite('C:/Users/Владимир/Desktop/Frame/Frame' + str(frameCounter) + '.jpg', frameCopy)
        frameCounter += 1
        (x, y, z, h) = cv.boundingRect(contours[0])  # добавляем к нашему контуру детектор, который подсвечивает более ярко
        cv.rectangle(frameCopy, (x, y), (x + z + 10, y + h - 3), (255, 0, 0), 2)
        cv.imshow("Rect", frameCopy)

# закрываем ненужные cv.imshow() для того, чтобы это не мешало нам смотреть результат работы


    #добавляем клавишу выключения
    if cv.waitKey(1)  == ord('q'):
        break

cap.release()
cv.destroyAllWindows() #закрываем все окна
