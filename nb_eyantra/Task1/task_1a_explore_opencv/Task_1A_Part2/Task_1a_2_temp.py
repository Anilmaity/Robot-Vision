import cv2
import os
import NB_247.Task1.task_1a_explore_opencv.Task_1A_Part2.Videos as path

vid_file_path =  path + 'ballmotion.m4v'
cap = cv2.VideoCapture(vid_file_path)
cap.set(1, 276)
_, frame = cap.read()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
cv2.imshow(hsv)
cv2.waitKey(0)