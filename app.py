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
from angle_detection import getAngle
from area_estimator import area_polygon, area_circle, area_irregular, image_preprocessing

lets_measure_app = Flask(__name__)


@lets_measure_app.route('/')
def index():
    return "Index of APi"


@lets_measure_app.route('/favicon.ico')
def favicon():
    return 'Favicon exception handler'


@lets_measure_app.route('/object_measurement_rectangle', methods=['POST'])
def dimension_measurement_rectangle():
    try:
        file = request.files['image']
    except requests.exceptions.RequestException as e:
        return jsonify({'msg': e, 'size': [None, None], 'image': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    opencv_image = generate_image_rectangle(opencv_image)
    return_value, image2str = cv2.imencode('.jpg', opencv_image)
    print("function was accessed")
    image_encode = base64.b64encode(image2str).decode()
    print(type(opencv_image))
    print(type(image2str))
    print(type(image_encode))
    return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode})


@lets_measure_app.route('/object_measurement_circle', methods=['POST'])
def dimension_measurement_circle():
    try:
        file = request.files['image']
    except requests.exceptions.RequestException as e:
        return jsonify(
            {'message': e, 'size': [None, None], 'image': None, 'no_of_circles': None, 'radius': None})
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    opencv_image, circle_detected, circle_x_y = generate_image_circle(opencv_image)
    return_value, image2str = cv2.imencode('.jpg', opencv_image)
    image_encode = base64.b64encode(image2str).decode()
    print("dimension_measurement_circle() was accessed")

    print(circle_detected)
    if circle_detected == -1:
        return jsonify(
            {'message': 'success', 'size': [w, h], 'image': image_encode, 'no_of_circles': -1, 'radius': None})
    elif circle_detected == 0:
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no_of_circles': circle_detected,
                        'radius': None})
    else:
        radius = []
        for i in circle_x_y:
            radius.append(i[2])
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no_of_circles': circle_detected,
                        'radius': radius})


@lets_measure_app.route('/colordetection', methods=['POST'])
def color_detection():
    try:
        file = request.files.get('image')
        request_data = request.form.to_dict()
    except requests.exceptions.Timeout as e1:
        return jsonify({'msg': e1, 'angle_value': None})
    except requests.exceptions.ConnectionError as e2:
        return jsonify({'msg': e2, 'angle_value': None})
    except requests.exceptions.HTTPError as e3:
        return jsonify({'msg': e3, 'angle_value': None})
    except requests.exceptions.RequestException as e4:
        return jsonify({'msg': e4, 'angle_value': None})

    # print(type(request_data))
    x = request_data['x-coord']
    y = request_data['y-coord']
    # print(x)
    # print(y)
    x_value = int(x)
    y_value = int(y)
    # print(type(x_value))
    # print(type(y_value))
    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    B, G, R = opencv_image[x_value, y_value]
    color_name = get_color_name(R, G, B)
    # print(type(B))
    # print(B)
    return jsonify(
        {'msg': 'success', 'color name': color_name, 'R-value': int(R), 'G-value': int(G), 'B-value': int(B)})


@lets_measure_app.route('/angledetector', methods=['POST'])
def angle_estimation():
    pointsList = []
    try:
        request_data = request.form.to_dict()
    except requests.exceptions.Timeout as e1:
        return jsonify({'msg': e1, 'angle_value': None})
    except requests.exceptions.ConnectionError as e2:
        return jsonify({'msg': e2, 'angle_value': None})
    except requests.exceptions.HTTPError as e3:
        return jsonify({'msg': e3, 'angle_value': None})
    except requests.exceptions.RequestException as e4:
        return jsonify({'msg': e4, 'angle_value': None})

    x1 = int(request_data['x1-coord'])
    y1 = int(request_data['y1-coord'])
    x2 = int(request_data['x2-coord'])
    y2 = int(request_data['y2-coord'])
    x3 = int(request_data['x3-coord'])
    y3 = int(request_data['y3-coord'])

    pointsList.append([x1, y1])
    pointsList.append([x2, y2])
    pointsList.append([x3, y3])

    if len(pointsList) == 3:
        angle_value = getAngle(pointsList)
        return jsonify({'msg': 'success', 'angle_value': int(angle_value)})
    return jsonify({'msg': 'did not receive provide 3 coordinate value for angle estimation', 'angle_value': None})


@lets_measure_app.route('/area_estimation_polygon', methods=['POST'])
def area_estimation_polygon():
    try:
        file = request.files['image']
    except requests.exceptions.RequestException as e:
        return jsonify({'msg': e, 'size': [None, None], 'image': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    image_canny = image_preprocessing(opencv_image)
    result_image, no_of_object, area_list = area_polygon(opencv_image, image_canny)
    return_value, image2str = cv2.imencode('.jpg', result_image)
    print("area_estimation_polygon was accessed")
    image_encode = base64.b64encode(image2str).decode()
    if no_of_object > 1:
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no of object': no_of_object,
                        'area-polygon': area_list})
    else:
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no of object': no_of_object,
                        'area-polygon': None})


@lets_measure_app.route('/area_estimation_circle', methods=['POST'])
def area_estimation_circle():
    try:
        file = request.files['image']
    except requests.exceptions.RequestException as e:
        return jsonify({'msg': e, 'size': [None, None], 'image': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    image_canny = image_preprocessing(opencv_image)
    result_image, circle_detected, circle_x_y_area = area_circle(opencv_image, image_canny)
    return_value, image2str = cv2.imencode('.jpg', result_image)
    print("area_estimation_circle() was accessed")
    image_encode = base64.b64encode(image2str).decode()

    if circle_detected > 0:
        area_list = []
        for i in circle_x_y_area:
            area_list.append(i[3])
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no_of_circles': circle_detected,
                        'Area-circle': area_list})
    else:
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no_of_circles': circle_detected,
                        'Area-circle': None})


if __name__ == "__main__":
    lets_measure_app.run(debug=True)
