import requests
from PIL import Image
import pickle
import base64
import json
from flask import jsonify

url = " http://127.0.0.1:5000/object_measurement_rectangle"


my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}

r = requests.post(url, files=my_img)
js = r.json()
imagereturn= js['image']

imdata = base64.b64decode(imagereturn)
print(type(imdata))
image = pickle.loads(imdata)

pilimage =Image.fromarray(image[...,::-1])
pilimage.show()
# print(r.json())

