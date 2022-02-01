import requests
from PIL import Image
import pickle
import base64
import json

url = "http://127.0.0.1:5000/area_estimation_polygon"

my_img = {'image': open('Testimages/aruco with hex2.png', 'rb')}

r = requests.post(url, files=my_img)
if r.ok:
    print("response received")
js = r.json()

if js['no of object'] == -1:
    print("No aruco")
elif js['no of object'] == 0:
    print("no object detected")
else:
    area_list = js['area-polygon']
    print(area_list)
    image_return = js['image']
    print(type(image_return))
    im_data = base64.b64decode(image_return)
    print(type(im_data))
    with open('resultofarea.jpg', 'wb') as file:
        file.write(im_data)
    print("file saved")


