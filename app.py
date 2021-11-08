from flask import Flask, jsonify, request, Response
import base64
import pickle
import cv2
from PIL import Image
import numpy as np
import requests
import json
from object_detector import HomogeneousBgDetector
from generate_image import generate_image_rectangle, generate_image_circle
from colorname_generator import get_color_name
app = Flask(__name__)

@app.route('/')
def index():
    return "Index of APi"

@app.route('/object_measurement_rectangle',methods= ['POST'])
def object_detection_rectangle():
    file = request.files['image']
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

    w = image.width
    h = image.height

    opencv_image = generate_image_rectangle(opencv_image)

    image2str=pickle.dumps(opencv_image)
    print("function was accessed")
    image_encode = base64.b64encode(image2str).decode('ascii')
    print(type(image_encode))
    print(image_encode)
    return jsonify({'message': 'success', 'size': [w,h],'image':base64.b64encode(image2str).decode('ascii')})

@app.route('/object_measurement_circle',methods=['POST'])
def object_measurement_circle():
    file = request.files['image']
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height

    opencv_image,circle_detected = generate_image_circle(opencv_image)
    print(circle_detected)

    opencv_image2str = pickle.dumps(opencv_image)
    print("function was accessed")

    image1_encode = base64.b64encode(opencv_image2str).decode('ascii')

    print(type(image1_encode))
    return jsonify({'message': 'success', 'size': [w,h],'image':base64.b64encode(opencv_image2str).decode('ascii'),'no_of_circles':circle_detected})


@app.route('/co lordetection', methods =['POST'])
def color_detection():
    file = request.files.get('image')
    request_data = request.json
    print(request_data)
    print(type(request_data))
    x = request_data['x-coord']
    print(x)
    y = request_data['y-coord']
    print(y)
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

    B,G,R = opencv_image [x,y]
    color_name = get_color_name(R,G,B)

    return jsonify({'msg': 'success', 'colorname':color_name, 'R-value':R,'G-value':G,'B-value':B})
    # return "Color Detection feature"

@app.route('/angledetector', methods =['POST'])
def angle_detection():

    return "This function returns angle value in degree between 2 edges"


if __name__ == "__main__":
    app.run(debug=True)
