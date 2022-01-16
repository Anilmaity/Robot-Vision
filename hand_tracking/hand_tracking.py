import cv2
import mediapipe as mp
import time



class handDetector:

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self, img, draw=True):

        self.results = self.hands.process(img)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, self.handLms, self.mphands.HAND_CONNECTIONS)
        return img

    def findpos(self, img, handno=0, draw=True):
        lmlist = []

        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmlist


def main():
    url = "http://192.168.43.1:8080/video"
    cap = cv2.VideoCapture(url)
    dectector = handDetector()

    st = 0
    tt = 0

    while True:
        success, img = cap.read()
        img = dectector.findhands(img)
        lmlist = dectector.findpos(img)
        if (len(lmlist) !=0):
            print(lmlist[4])

        st = time.time()
        fps = 1 / (st - tt)
        tt = st
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        if img is not None:
            cv2.imshow("Frame", img)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
