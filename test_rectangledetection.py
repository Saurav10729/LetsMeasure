import requests
from PIL import Image
import pickle
import base64
import json

url = "http://2565-110-44-116-42.ngrok.io/object_measurement_rectangle"


my_img = {'image': open('Testimages\imagewithcircle_aruco.jpg', 'rb')}

r = requests.post(url, files=my_img)
if( r.ok):
    print("response recieved")
js = r.json()

imagereturn= js['image']
print(type(imagereturn))
imdata = base64.b64decode(imagereturn)
# print(imdata)
print(type(imdata))
# image = pickle.loads(imdata)
# print(js)
# pilimage =Image.fromarray(image[...,::-1])    
# pilimage.show()
with open('result.jpg','wb') as file:
    file.write(imdata)
print("file saved")
f= open('b64.txt','w')
f.write(imagereturn)
f.close()
print("b64 saved")