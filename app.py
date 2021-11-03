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

    opencv_image,opencv_detectedcircle = generate_image_circle(opencv_image)
    cv2.imshow(opencv_image)
    cv2.imshow(opencv_detectedcircle)

    opencv_image2str = pickle.dumps(opencv_image)
    elipse_image2str=pickle.dumps(opencv_detectedcircle)
    print("function was accessed")

    image1_encode = base64.b64encode(opencv_image2str).decode('ascii')
    image2_encode = base64.b64encode(elipse_image2str).decode('ascii')

    print(type(image1_encode))
    print(type(image2_encode))
    return jsonify({'message': 'success', 'size': [w,h],'image1':base64.b64encode(opencv_image2str).decode('ascii'),'image2':base64.b64encode(elipse_image2str).decode('ascii')})


    # return "This function returns RGB value for a x,y coordinate in the image provided"


@app.route('/colordetection', methods =['POST'])
def color_detection():
    # # return "This function returns RGB value for a x,y coordinate in the image provided"
    # file = request.files['image']
    # request_data = request.get_json(silent=True)
    # print(type(request_data))
    # x = request_data['x-coord']
    # y = request_data['y-coord']
    #
    # image = Image.open(file.stream)
    # opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    #
    # B,G,R = opencv_image [x,y]
    # color_name = get_color_name(R,G,B)
    # #
    # # return jsonify({'msg': 'success'})
    # return jsonify({'msg': 'success', 'size': [w, h], 'colorname':color_name, 'R-value':R,'G-value':G,'B-value':B})
    return "Color Detection feature"

@app.route('/angledetector', methods =['POST'])
def angle_detection():

    return "This function returns angle value in degree between 2 edges"


if __name__ == "__main__":
    app.run(debug=True)
