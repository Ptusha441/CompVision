import cv2
import mediapipe as mp
import keyboard
from time import sleep
import winsound

camera = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

points = [0 for i in range(21)]
points_x = [0 for i in range(21)]
finger = [0 for i in range(5)]

flagR = False
flagL = False

def distance(point1, point2):
    return abs(point1 - point2)

while True:
    good, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, point in enumerate(handLms.landmark):
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)

                points[id] = height

                # Рисование кружочков на кончиках пальцев
                # points_x[id] = width
                # if id == 8:
                #     cv2.circle(img, (width, height), 15, (255, 0, 255), cv2.FILLED)
                # if id == 12:
                #     cv2.circle(img, (width, height), 15, (0, 0, 255), cv2.FILLED)


        distanceGood = distance(points[0], points[5]) + (distance(points[0], points[5])/2)

        finger[1] = 1 if distance(points[0], points[8]) > distanceGood else 0  # указательный
        finger[2] = 1 if distance(points[0], points[12]) > distanceGood else 0 # средний
        finger[3] = 1 if distance(points[0], points[16]) > distanceGood else 0 # безымянный
        finger[4] = 1 if distance(points[0], points[20]) > distanceGood else 0 # мизинец
        finger[0] = 1 if distance(points[4], points[17]) > distanceGood else 0 # большой


        # Сырая реализация переключения переместив два пальца
        if (finger[0], finger[1], finger[2], finger[3], finger[4]) == (0,1,1,0,0):
            # print(points[8])
            if point.x < 0.2:
                flagR = True
                # winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                winsound.MessageBeep()
            if point.x > 0.7 and flagR == True:
                flagL = True
                # winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                winsound.MessageBeep()
            # print(point.x, flagR, flagL)


        if flagR and flagL:
            print("RIGHT")
            keyboard.send("right")
            flagR = False
            flagL = False
            # input()

        if (finger[0], finger[1], finger[2], finger[3], finger[4]) == (0, 0, 0, 0, 0):
            flagR = False
            flagL = False

    # Вывод камеры на экран
    # cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break
