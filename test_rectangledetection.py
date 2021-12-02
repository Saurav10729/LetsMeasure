import requests
from PIL import Image
import pickle
import base64
import json

url = "http://9f92-43-245-87-205.ngrok.io/object_measurement_rectangle"

my_img = {'image': open('Testimages/laptopwitharuco.jpg', 'rb')}

r = requests.post(url, files=my_img)
if r.ok:
    print("response recieved")
js = r.json()

image_return = js['image']
print(type(image_return))
im_data = base64.b64decode(image_return)
# print(imdata)
print(type(im_data))
# image = pickle.loads(imdata)
# print(js)
# pilimage =Image.fromarray(image[...,::-1])    
# pilimage.show()
with open('result.jpg', 'wb') as file:
    file.write(im_data)
print("file saved")
f = open('b64.txt', 'w')
f.write(image_return)
f.close()
print("b64 saved")
