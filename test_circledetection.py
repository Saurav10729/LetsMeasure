import requests
from PIL import Image
import pickle
import base64
import json
from flask import jsonify
url = "http://127.0.0.1:5000/object_measurement_circle"

my_img = {'image': open('Testimages\image_with_aruco_button.jpg', 'rb')}
r = requests.post(url, files=my_img)
js = r.json()

if(js['no_of_circles']==-1):
    print("No Aruco Marker was spoted")
elif(js['no_of_circles']==0):
    print("no circles were detected in the image")
else:
    imagereturn= js['image']
    imdata = base64.b64decode(imagereturn)
    print(type(imdata))
    # image = pickle.loads(imdata)
    # pilimage =Image.fromarray(image[...,::-1])
    # pilimage.show()
    with open('circleresult.jpg','wb') as file:
        file.write(imdata)
