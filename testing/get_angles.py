import requests
import time
url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id_no': '00'}

x = requests.post(url, data = myobj)


def get_angles():
    start = time.time()
    x = requests.post(url, data=myobj)
    end = time.time()
    print(end - start)

while True:
    get_angles()

