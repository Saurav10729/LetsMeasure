import requests
from PIL import Image
import pickle
import base64
import json

url = "http://127.0.0.1:5000/object_measurement_rectangle"
my_img = {'image': open('Testimages/aruco_only2.jpg', 'rb')}
r = requests.post(url, files=my_img)
if r.ok:
    print("response received")
js = r.json()
if js['message'] == 'success':
    if js['no of object'] >1:
        image_return = js['image']
        print(type(image_return))
        im_data = base64.b64decode(image_return)
        print(type(im_data))
        with open('result_dimension_polygon.jpg', 'wb') as file:
            file.write(im_data)
    elif js['no of object']== -1:
        print("No ArUco found")
else:
    print(js['message'])

print("file saved")
