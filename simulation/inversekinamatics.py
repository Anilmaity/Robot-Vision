import math
from math import sin, cos
import numpy as np


def calculate_HTM(frame):
    H_matrix = []

    for frames in frame:
        H_matrix.append(h_matrix(frames[0], frames[1], frames[2], frames[3]))

    HTM = H_matrix[0]

    for i in range(len(H_matrix) - 1):
        HTM = np.dot(HTM, H_matrix[i + 1])

    # print(HTM)
    return HTM


def h_matrix(theta, alpha, r, d):
    theta = (theta * math.pi) / 180
    alpha = (alpha * math.pi) / 180

    H = np.array([[cos(theta), - sin(theta) * cos(alpha), sin(theta) * sin(alpha), r * cos(theta)],
                  [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), r * sin(theta)],
                  [0, sin(alpha), cos(alpha), d],
                  [0, 0, 0, 1]])
    #print(H)
    return H

'''
              d         theta           a(r)        alpha
   1and2     0.0880      90.           0.0003      90.0 
   2and3      0          90              0.2101     0
   3and4       0.0006     0.1              0.0300   90
   4and5         0.2214    168.8            0.009    90
   5and6       -0.0001      -178           0.0005     90


'''


frames = [[90, 90, 0.003, 0.0880],
          [90, 0, 0.2101, 0],
          [0.1, 90, 0.0300, 0.0006],
          [168.8, 90, 0.009, 0.2214],
          [-178, 90, 0.0005, -0.0001]]


print(sin(math.pi / 2))
print(calculate_HTM(frames))
