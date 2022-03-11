import cv2 as cv
import mediapipe as mp
import time
import gc

buttons = [False, False, False, False, False]


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, image, draw=True):
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        image, hand, self.mpHands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, handNo=0, draw=True):
        x = []
        y = []
        h, w, c = image.shape
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, land in enumerate(myHand.landmark):
                cx, cy = int(land.x * w), int(land.y * h)
                x.append(cx)
                y.append(cy)

                if draw:
                    cv.circle(image, (cx, cy), 15, (0, 0, 255), cv.FILLED)

            self.button_condition(x, y)

            print(buttons)

        return x, y

    def button_condition(self, x, y):
        global buttons
        l = [8, 12, 16, 20]
        l_c = [7, 11, 15, 19]
        d = []
        d_c = []

        for i in range(0, 4):

            d.append(abs(x[l[i]] - x[0]) + abs(y[l[i]] - y[0]))
            d_c.append(abs(x[l_c[i]] - x[0]) + abs(y[l_c[i]] - y[0]))
            # print(d_1,d_c_1)
            if d[i] > d_c[i]:
                buttons[i] = True
            else:
                buttons[i] = False


def main():
    url = "http://192.168.43.1:8080/video"
    cap = cv.VideoCapture(0)
    ret = 1
    pre_time = time.time()
    gc.enable()
    handDtc = handDetector()

    while ret:
        ret, frame = cap.read()
        crt_time = time.time()

        tt = int((crt_time-pre_time)*1000)
        fps = int((1/tt)*1000)
        image = handDtc.findHands(frame)
        lmList = handDtc.findPosition(image)
        cv.putText(image, str(fps), (50, 50),
                   cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
        image = frame
        cv.imshow('image', image)
        pre_time = time.time()
        if cv.waitKey(1) == ord('q'):
            ret = False
            # print(lmList)

        del image
        gc.collect()


if __name__ == "__main__":
    main()
