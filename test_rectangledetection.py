import requests
from PIL import Image
import pickle
import base64
import json

url = " http://6c4e-110-44-127-181.ngrok.io/object_measurement_rectangle"


my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}

r = requests.post(url, files=my_img)
js = r.json()
imagereturn= js['image']

imdata = base64.b64decode(imagereturn)
print(type(imdata))
image = pickle.loads(imdata)
print(imdata)
pilimage =Image.fromarray(image[...,::-1])

pilimage.show()
