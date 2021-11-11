import requests
from PIL import Image
import pickle
import base64
import json
from flask import jsonify
url = "http://240d-103-10-31-50.ngrok.io/object_measurement_circle"

my_img = {'image': open('Testimages\imagewithcircle_aruco.jpg', 'rb')}
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
