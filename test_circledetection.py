import requests
from PIL import Image
import pickle
import base64
import json
from flask import jsonify

url = " http://127.0.0.1:5000/object_measurement_circle"

my_img = {'image': open('Testimages/aruco_only3.jpg', 'rb')}

r = requests.post(url, files=my_img)
js = r.json()
print("CLIENT >>>")
if js['no of object'] == -1:
    print("No Aruco Marker was spotted")
elif js['no of object'] == 0:
    print("no circles were detected in the image")
else:
    image_return = js['image']
    im_data = base64.b64decode(image_return)
    circle_radius = js['radius']
    count = 1
    for i in circle_radius:
        print("Radius of Circle", count, " : ", i)
        count += 1
    print(type(im_data))

    with open('result_dimension_circle.jpg', 'wb') as file:
        file.write(im_data)
