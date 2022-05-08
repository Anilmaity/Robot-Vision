import pandas as pd
import yolov5
import cv2
import time
from inverse_kinematics import inverse_kinematics

url = "http://192.168.43.1:8080/video"
cap = cv2.VideoCapture(url)
import requests
import time

url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id_no': '00'}

Joints = [0, 0, 0, 0, 0, 0]
x = requests.post(url, data=myobj)

print(x.text)


def get_angles():
    x = requests.post(url, data=myobj)
    print(x.text)
    time.sleep(1)


def set_angles(angles):
    x = requests.post(url, data=angles)
    data = x.json()
    print(data)


# load model
model = yolov5.load('yolov5s.pt')

pre_time = 1

while True:

    crt_time = time.time()

    tt = int((crt_time - pre_time) * 1000)
    fps = int((1 / tt) * 1000)
    pre_time = crt_time
    success, img = cap.read()
    # print(img.shape)

    results = model(img)
    result = results.pandas().xyxy[0]  # img1 predictions (pandas)
    rest = pd.DataFrame(result)
    # print(rest)
    object_pick_list = ['ball']

    for i, obj in enumerate(rest.iloc):
        # print(obj)
        # print((int(obj['xmin']), int(obj['ymin'])),(int(obj['xmax']), int(obj['ymax'])) )
        if (obj['name'] == object_pick_list[0]):
            object_ = obj['name']
            xposition = (obj['xmin'] + obj['xmax']) / 2
            yposition = (obj['ymin'] + obj['ymax']) / 2
            yposition_cm = 15 + (-50 * ((((obj['xmin'] + obj['xmax']) / 2) - 256) / 256))
            xposition_cm = 40 + (-50 * ((((obj['ymin'] + obj['ymax']) / 2) - 256) / 256))
            zposition_cm = 16.5
            angle_initiatializer = inverse_kinematics.get_robot_angles(
                xposition_cm, yposition_cm, zposition_cm, 'left')
            print(angle_initiatializer)

        cv2.rectangle(img, (int(obj['xmin']), int(obj['ymin'])), (int(
            obj['xmax']), int(obj['ymax'])), (0, 0, 255), 2)
        cv2.putText(img, obj['name'] + "  " + str(round(obj['confidence'], 2)), (int(
            obj['xmin']), int(obj['ymin'])), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

    cv2.putText(img, str(fps), (50, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

    # print(results)

    if img is not None:
        cv2.imshow("Frame", img)
    q = cv2.waitKey(1)
    if q == ord("q"):
        break

cv2.destroyAllWindows()
