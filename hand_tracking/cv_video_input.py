import cv2
import os
url = "http://192.168.43.1:8080/video"
cap = cv2.VideoCapture(url)


while True:
    success, img = cap.read()

    if img is not None:
        cv2.imshow("Frame", img)
    q = cv2.waitKey(1)
    if q == ord("q"):
        break
cv2.destroyAllWindows()


def create_log_file(file_name):
    # check log file
    if not os.path.exists(file_name):
        # create log file

        with open(file_name, "w") as f:
            f.write("")
    else:
        log_file = open(file_name, "a")
        log_file.write("\n")
        log_file.close()


    with open(file_name, "w") as f:
        f.write("")