import requests
from PIL import Image
import pickle
import base64
import json

url = "http://127.0.0.1:5000/area_estimation_circle"

<<<<<<< HEAD
my_img = {'image': open('Testimages/aruco_with_circle_highres.jpg', 'rb')}
=======
my_img = {'image': open('Testimages/aruco_with_cap.jpg', 'rb')}
>>>>>>> 21c3336a0a9d5866f9362d11f0c6ec80cdc11b72

r = requests.post(url, files=my_img)
if r.ok:
    print("response received")
js = r.json()

if js['no of object'] == -1:
    print("No aruco")
elif js['no of object'] == 0:
    print("no circles detected")
else:
    area_list = js['area-circle']
    perimeter_list = js ['perimeter-circle']
    print(area_list)
    image_return = js['image']
    print(type(image_return))
    im_data = base64.b64decode(image_return)
    print(type(im_data))
    with open('result_area_circle.jpg', 'wb') as file:
        file.write(im_data)
    print("file saved")
