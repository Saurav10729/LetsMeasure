import requests
from PIL import Image
import pickle
import base64
import json
from flask import jsonify


# Request sent for testing object_measurement_rectangle route of the api
# url = " http://6913-110-44-116-42.ngrok.io/object_measurement_rectangle"
#
#
# my_img = {'image': open('Testimages\laptopwitharuco.jpg', 'rb')}
#
# r = requests.post(url, files=my_img)
# js = r.json()
# imagereturn= js['image']
#
# imdata = base64.b64decode(imagereturn)
# print(type(imdata))
# image = pickle.loads(imdata)
#
# pilimage =Image.fromarray(image[...,::-1])
# pilimage.show()

#Request sent for testing object_measurement_circle route of the api
url = " http://6913-110-44-116-42.ngrok.io/object_measurement_circle"


my_img = {'image': open('Testimages\pexels-photo-257897.jpeg', 'rb')}

r = requests.post(url, files=my_img)
js = r.json()
imagereturn_contour= js['image1']
imagereturn_ellipse= js['image2']

imdata1 = base64.b64decode(imagereturn_contour)
imdata2 = base64.b64decode(imagereturn_ellipse)

image1 = pickle.loads(imdata1)
image2 = pickle.load(imdata2)

pilimage1 =Image.fromarray(image1[...,::-1])
pilimage2 =Image.fromarray(image2[...,::-1])

pilimage1.show()
pilimage2.show()



# print(r.json())

