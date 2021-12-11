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
from angle_detection import gradient, get_angle
lets_measure_app = Flask(__name__)


@lets_measure_app.route('/')
def index():
    return "Index of APi"


@lets_measure_app.route('/favicon.ico')
def favicon():
    return 'Favicon exception handler'


@lets_measure_app.route('/object_measurement_rectangle', methods=['POST'])
def object_detection_rectangle():
    file = request.files['image']
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    opencv_image = generate_image_rectangle(opencv_image)
    retval, image2str = cv2.imencode('.jpg', opencv_image)
    print("function was accessed")
    image_encode = base64.b64encode(image2str).decode()
    print(type(opencv_image))
    print(type(image2str))
    print(type(image_encode))
    return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode})


@lets_measure_app.route('/object_measurement_circle', methods=['POST'])
def object_measurement_circle():
    file = request.files['image']
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    opencv_image, circle_detected, circle_x_y = generate_image_circle(opencv_image)
    print(circle_detected)
    radius = []
    for i in circle_x_y:
        radius.append(i[2])
    retval, image2str = cv2.imencode('.jpg', opencv_image)
    image_encode = base64.b64encode(image2str).decode()
    print("function was accessed")
    return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no_of_circles': circle_detected,
                    'radius': radius})


@lets_measure_app.route('/colordetection', methods=['POST'])
def color_detection():
    file = request.files.get('image')
    request_data = request.form.to_dict()
    print(type(request_data))
    x = request_data['x-coord']
    y = request_data['y-coord']
    print(x)
    print(y)
    x_value = int(x)
    y_value = int(y)
    print(type(x_value))
    print(type(y_value))
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    B, G, R = opencv_image[x_value, y_value]
    color_name = get_color_name(R, G, B)
    print(type(B))
    print(B)
    return jsonify({'msg': 'success', 'colorname': color_name, 'R-value': int(R), 'G-value': int(G), 'B-value': int(B)})


@lets_measure_app.route('/angledetector', methods=['POST'])
def angle_detection():
    pointsList = []
    request_data = request.form.to_dict()

    x1 = int(request_data['x1-coord'])
    y1 = int(request_data['y1-coord'])
    x2 = int(request_data['x2-coord'])
    y2 = int(request_data['y2-coord'])
    x3 = int(request_data['x3-coord'])
    y3 = int(request_data['y3-coord'])

    pointsList.append([x1, y1])
    pointsList.append([x2, y2])
    pointsList.append([x3, y3])
    if (len(pointsList)==3):
        angle_value = get_angle(pointsList)
        return jsonify({'msg': 'success', 'angle_value':angle_value})
    return  jsonify({'msg': '3 coordinates are needed for angle estimation', 'angle_value':None})

if __name__ == "__main__":
    lets_measure_app.run(debug=True)
