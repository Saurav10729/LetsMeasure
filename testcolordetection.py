import requests
from PIL import Image
import pickle
import base64
import json

url="http://aa57-103-10-31-50.ngrok.io/colordetection"
my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}
x = 100
y = 150

# header = {'Content-type':'application/json'}
x_str = str(x)
y_str = str(y)

datas = {
    'msge':'sent',
    'x-coord':x_str,
    'y-coord':y_str
}
print("done")
r = requests.post(url, files=my_img, data = datas)
if r.ok:
    print("request sent")
    print(r.json())
js = r.json()
#
messagereturned =js['msg']
print(messagereturned)
# R = js['R-value']
# G = js['G-value']
# B = js['B-value']
# color_name = js['colorname']
#
# print('R-value:',R)
# print('G-value:',G)
# print('B-value:',B)
# print('Color name:',color_name)


