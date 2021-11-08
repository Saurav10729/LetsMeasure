import requests
from PIL import Image
import pickle
import base64
import json

url="http://0460-110-44-116-42.ngrok.io/colordetection"
my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}
x,y =100,150

header = {'Content-type':'application/json'}
datas = {"data":{"msge":"sent","x-coord":x,"y-coord":y}}

r = requests.post(url, files=my_img, json =json.dumps(datas), headers=header)
if r.ok:
    print(r.json())
js = r.json()
messagereturned =js['msg']
R = js['R-value']
G = js['G-value']
B = js['B-value']
color_name = js['colorname']

print('R-value:',R)
print('G-value:',G)
print('B-value:',B)
print('Color name:',color_name)


