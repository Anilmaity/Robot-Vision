import requests
import time
import os
url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id_no': '00'}

x = requests.post(url, data = myobj)

print(x.text)


def write_to_file(file_name, data):
    f = open(file_name, 'a')
    now = time.strftime("%c")
    f.write(str(now) + "  " + str(data) + "\n")
    f.close()


# create a function to check file exist or not
def check_file_exist(file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False


# create a function to create file
def create_file(file_name, data):
    if check_file_exist(file_name):
        write_to_file(file_name, data)
    else:
        f = open(file_name, 'w')
        f.close()
        write_to_file(file_name, data)

print(time.strftime("%d-%m-%Y"))
try:
    while (True):
        x = requests.post(url, data=myobj)
        print(x.text)
        todays_date = time.strftime("%d-%m-%Y")
        create_file('Logs\\'+str(todays_date), x.text)

except KeyboardInterrupt:
        print("\nExiting...")

