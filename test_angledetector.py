import requests
from PIL import Image
import pickle
import base64
import json

url = "http://127.0.0.1:5000/angledetector"

x1, x2, x3 = 30, 10, 10
y1, y2, y3 = 10, 10, 28

data_value = {
    'message': 'sent',
    'x1-coord': str(x1),
    'y1-coord': str(y1),
    'x2-coord': str(x2),
    'y2-coord': str(y2),
    'x3-coord': str(x3),
    'y3-coord': str(y3)
}
print("done")
r = requests.post(url, data=data_value)
if r.ok:
    print("request sent")
    print(r.json())
js = r.json()
if js['message'] == "did not receive provide 3 coordinate value for angle estimation":
    print("Oops, it seems that you did not provide 3 coordinates")
else:
    angle = js['angle_value']
    print("angle between x1,y1 , x2,y2 and x3,y3 was found to be", angle, u"\N{DEGREE SIGN}")
