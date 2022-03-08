# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.
Usage - sources:
    $ python path/to/detect.py --weights yolov5s.pt --source 0              # webcam
                                                             img.jpg        # image
                                                             vid.mp4        # video
                                                             path/          # directory
                                                             path/*.jpg     # glob
                                                             'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                             'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
Usage - formats:
    $ python path/to/detect.py --weights yolov5s.pt                 # PyTorch
                                         yolov5s.torchscript        # TorchScript
                                         yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                         yolov5s.xml                # OpenVINO
                                         yolov5s.engine             # TensorRT
                                         yolov5s.mlmodel            # CoreML (MacOS-only)
                                         yolov5s_saved_model        # TensorFlow SavedModel
                                         yolov5s.pb                 # TensorFlow GraphDef
                                         yolov5s.tflite             # TensorFlow Lite
                                         yolov5s_edgetpu.tflite     # TensorFlow Edge TPU


ID	OBJECT (PAPER)	OBJECT (2014 REL.)	OBJECT (2017 REL.)	SUPER CATEGORY
1	person	person	person	person
2	bicycle	bicycle	bicycle	vehicle
3	car	car	car	vehicle
4	motorcycle	motorcycle	motorcycle	vehicle
5	airplane	airplane	airplane	vehicle
6	bus	bus	bus	vehicle
7	train	train	train	vehicle
8	truck	truck	truck	vehicle
9	boat	boat	boat	vehicle
10	traffic light	traffic light	traffic light	outdoor
11	fire hydrant	fire hydrant	fire hydrant	outdoor
12	street sign	-	-	outdoor
13	stop sign	stop sign	stop sign	outdoor
14	parking meter	parking meter	parking meter	outdoor
15	bench	bench	bench	outdoor
16	bird	bird	bird	animal
17	cat	cat	cat	animal
18	dog	dog	dog	animal
19	horse	horse	horse	animal
20	sheep	sheep	sheep	animal
21	cow	cow	cow	animal
22	elephant	elephant	elephant	animal
23	bear	bear	bear	animal
24	zebra	zebra	zebra	animal
25	giraffe	giraffe	giraffe	animal
26	hat	-	-	accessory
27	backpack	backpack	backpack	accessory
28	umbrella	umbrella	umbrella	accessory
29	shoe	-	-	accessory
30	eye glasses	-	-	accessory
31	handbag	handbag	handbag	accessory
32	tie	tie	tie	accessory
33	suitcase	suitcase	suitcase	accessory
34	frisbee	frisbee	frisbee	sports
35	skis	skis	skis	sports
36	snowboard	snowboard	snowboard	sports
37	sports ball	sports ball	sports ball	sports
38	kite	kite	kite	sports
39	baseball bat	baseball bat	baseball bat	sports
40	baseball glove	baseball glove	baseball glove	sports
41	skateboard	skateboard	skateboard	sports
42	surfboard	surfboard	surfboard	sports
43	tennis racket	tennis racket	tennis racket	sports
44	bottle	bottle	bottle	kitchen
45	plate	-	-	kitchen
46	wine glass	wine glass	wine glass	kitchen
47	cup	cup	cup	kitchen
48	fork	fork	fork	kitchen
49	knife	knife	knife	kitchen
50	spoon	spoon	spoon	kitchen
51	bowl	bowl	bowl	kitchen
52	banana	banana	banana	food
53	apple	apple	apple	food
54	sandwich	sandwich	sandwich	food
55	orange	orange	orange	food
56	broccoli	broccoli	broccoli	food
57	carrot	carrot	carrot	food
58	hot dog	hot dog	hot dog	food
59	pizza	pizza	pizza	food
60	donut	donut	donut	food
61	cake	cake	cake	food
62	chair	chair	chair	furniture
63	couch	couch	couch	furniture
64	potted plant	potted plant	potted plant	furniture
65	bed	bed	bed	furniture
66	mirror	-	-	furniture
67	dining table	dining table	dining table	furniture
68	window	-	-	furniture
69	desk	-	-	furniture
70	toilet	toilet	toilet	furniture
71	door	-	-	furniture
72	tv	tv	tv	electronic
73	laptop	laptop	laptop	electronic
74	mouse	mouse	mouse	electronic
75	remote	remote	remote	electronic
76	keyboard	keyboard	keyboard	electronic
77	cell phone	cell phone	cell phone	electronic
78	microwave	microwave	microwave	appliance
79	oven	oven	oven	appliance
80	toaster	toaster	toaster	appliance
81	sink	sink	sink	appliance
82	refrigerator	refrigerator	refrigerator	appliance
83	blender	-	-	appliance
84	book	book	book	indoor
85	clock	clock	clock	indoor
86	vase	vase	vase	indoor
87	scissors	scissors	scissors	indoor
88	teddy bear	teddy bear	teddy bear	indoor
89	hair drier	hair drier	hair drier	indoor
90	toothbrush	toothbrush	toothbrush	indoor
91	hair brush	-	-

"""


import pandas as pd
import yolov5
import cv2
import time

url = "http://192.168.43.1:8080/video"
cap = cv2.VideoCapture(0)


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
    for i, obj in enumerate(rest.iloc):
        # print(obj)
        #print((int(obj['xmin']), int(obj['ymin'])),(int(obj['xmax']), int(obj['ymax'])) )

        cv2.rectangle(img, (int(obj['xmin']), int(obj['ymin'])), (int(
            obj['xmax']), int(obj['ymax'])), (0, 0, 255), 2)
        cv2.putText(img, obj['name']+"  "+str(round(obj['confidence'], 2)), (int(
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
