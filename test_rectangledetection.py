import requests
from PIL import Image
import pickle
import base64
import json

url = "http://aa57-103-10-31-50.ngrok.io/object_measurement_rectangle"


my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}

r = requests.post(url, files=my_img)
if( r.ok):
    print("response recieved")
    js = r.json()

imagereturn= js['image']
print(type(imagereturn))
imdata = base64.b64decode(imagereturn)
# print(imdata)
print(type(imdata))
image = pickle.loads(imdata)
# print(js)
pilimage =Image.fromarray(image[...,::-1])

pilimage.show()
