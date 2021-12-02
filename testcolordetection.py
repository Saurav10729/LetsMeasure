import requests
import pickle
import base64
import json

url = "http://127.0.0.1:5000/colordetection"
my_img = {'image': open('Testimages/laptopwitharuco.jpg', 'rb')}
x = 100
y = 121
datas = {
    'msge': 'sent',
    'x-coord': str(x),
    'y-coord': str(y)
}
print("done")
r = requests.post(url, files=my_img, data=datas)
if r.ok:
    print("request sent")
    print(r.json())
js = r.json()

messagereturned = js['msg']
print(messagereturned)
R = js['R-value']
G = js['G-value']
B = js['B-value']
color_name = js['colorname']

print('R-value:', R)
print('G-value:', G)
print('B-value:', B)
print('Color name:', color_name)
