import requests

url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id': '0'}

x = requests.post(url, data = myobj)

print(x)