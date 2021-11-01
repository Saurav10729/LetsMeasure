import requests
from PIL import Image
import pickle
import base64
import json


url = " http://127.0.0.1:5000/colordetection"


my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}

x,y =100,150    #the coordinates whose RGB, color value is needed

data = {'msge':'sent','x-coord':x,'y-coord':y}
# jsondata =json.dumps((data))
r = requests.post(url, files=my_img, json={'msge':'sent','x-coord':x,'y-coord':y})
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


