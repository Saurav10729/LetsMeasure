import requests
from PIL import Image
import pickle
import base64
import json

url = "http://a028-103-10-31-55.ngrok.io/object_measurement_rectangle"

my_img = {'image': open('Testimages/rotated_aruco_with_coaster.jpg', 'rb')}

r = requests.post(url, files=my_img)
if r.ok:
    print("response received")
js = r.json()

image_return = js['image']
print(type(image_return))
im_data = base64.b64decode(image_return)
print(type(im_data))
with open('result.jpg', 'wb') as file:
    file.write(im_data)
print("file saved")
