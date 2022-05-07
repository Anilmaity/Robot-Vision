import requests
import time
url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id_no': '00'}

x = requests.post(url, data = myobj)

print(x.text)

def get_angles():
    x = requests.post(url, data=myobj)
    print(x.text)
    time.sleep(1)
