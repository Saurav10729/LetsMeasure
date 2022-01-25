import requests
from PIL import Image
import pickle
import base64
import json

url = "http://127.0.0.1:5000/area_estimation_polygon"

my_img = {'image': open('Testimages/phone_with_aruco.jpg', 'rb')}

r = requests.post(url, files=my_img)
if r.ok:
    print("response recieved")
js = r.json()

area_list = js['area-polygon']
print(area_list)
image_return = js['image']
print(type(image_return))
im_data = base64.b64decode(image_return)
print(type(im_data))
with open('resultofarea.jpg', 'wb') as file:
    file.write(im_data)
print("file saved")
f = open('b64.txt', 'w')
f.write(image_return)
f.close()
print("b64 saved")
