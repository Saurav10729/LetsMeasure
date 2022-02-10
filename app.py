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
def dimension_measurement_polygon():
    try:
        file = request.files['image']
    except requests.exceptions.Timeout:
        return jsonify({'message': 'Oops! it client-server connection timeout occurred.',
                        'image': None, 'no of object': None, "dimensional data": None})

    except requests.exceptions.ConnectionError:
        return jsonify({'message': 'There seems to be a connection error.  Check your internet connection',
             'image': None, 'no of object': None, "dimensional data": None})

    except requests.exceptions.HTTPError:
        return jsonify({'message': 'Http Connection Error occurred.  Check your internet connection',
             'image': None, 'no of object': None, "dimensional data": None})

    except requests.exceptions.RequestException:
        return jsonify({'message': 'A RequestException occurred. Check your internet connection',
                        'image': None, 'no of object': None, "dimensional data": None})

    print("dimension_measurement_polygon() was accessed")

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    opencv_image, no_of_object, dimension_list = generate_image_rectangle(opencv_image)

    return_value, image2str = cv2.imencode('.jpg', opencv_image)
    image_encode = base64.b64encode(image2str).decode()
    print("no of object",no_of_object)
    if no_of_object > 1:
        return jsonify({'message': 'success', 'image': image_encode, 'no of object': no_of_object,
                        "dimensional data": dimension_list})

    elif no_of_object == 1:
        return jsonify({'message': 'Both ArUco and Object should be present', 'image': None, 'no of object': no_of_object,
                        "dimensional data": None})
    else:
        return jsonify({'message': 'success', 'image': None,
                        'no of object': no_of_object,
                        "dimensional data": None})

@lets_measure_app.route('/object_measurement_circle', methods=['POST'])
def dimension_measurement_circle():
    try:
        file = request.files['image']
    except requests.exceptions.Timeout:
        return jsonify(
            {'message': 'Oops! it client-server connection timeout occurred.',   'image': None,
             'no of object': None,
             'radius': None})
    except requests.exceptions.ConnectionError:
        return jsonify(
            {'message': 'There seems to be a connection error.  Check your internet connection',
             'image': None, 'no of object': None,
             'radius': None})
    except requests.exceptions.HTTPError:
        return jsonify(
            {'message': 'Http Connection Error occurred.  Check your internet connection',
             'image': None, 'no of object': None,
             'radius': None})
    except requests.exceptions.RequestException:
        return jsonify(
            {'message': 'A RequestException occurred. Check your internet connection',
             'image': None, 'no of object': None,'radius': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    opencv_image, no_of_object, circle_x_y = generate_image_circle(opencv_image)
    return_value, image2str = cv2.imencode('.jpg', opencv_image)
    image_encode = base64.b64encode(image2str).decode()
    print("dimension_measurement_circle() was accessed")

    print("No of objects: ",no_of_object)
    if no_of_object >= 1:
        radius = []
        for i in circle_x_y:
            radius.append(i[2])
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no of object': no_of_object,
                        'radius': radius})
    else:
        return jsonify({'message': 'success', 'size': [w, h], 'image': None, 'no of object': no_of_object,
             'radius': None})


@lets_measure_app.route('/colordetection', methods=['POST'])
def color_detection():
    try:
        file = request.files.get('image')
        request_data = request.form.to_dict()
    except requests.exceptions.Timeout:
        return jsonify(
            {'message': 'Oops! it client-server connection timeout occurred.', 'color name': None, 'R-value': None,
             'G-value': None, 'B-value': None})
    except requests.exceptions.ConnectionError:
        return jsonify(
            {'message': 'There seems to be a connection error.  Check your internet connection', 'color name': None,
             'R-value': None, 'G-value': None, 'B-value': None})
    except requests.exceptions.HTTPError:
        return jsonify(
            {'message': 'Http Connection Error occurred.  Check your internet connection', 'color name': None,
             'R-value': None, 'G-value': None, 'B-value': None})
    except requests.exceptions.RequestException:
        return jsonify(
            {'message': 'A RequestException occurred. Check your internet connection', 'color name': None,
             'R-value': None, 'G-value': None, 'B-value': None})

    x = request_data['x-coord']
    y = request_data['y-coord']

    x_value = int(x)
    y_value = int(y)

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    B, G, R = opencv_image[x_value, y_value]
    color_name = get_color_name(R, G, B)

    return jsonify(
        {'message': 'success', 'color name': color_name, 'R-value': int(R), 'G-value': int(G), 'B-value': int(B)})


@lets_measure_app.route('/angledetector', methods=['POST'])
def angle_estimation():
    pointsList = []
    try:
        request_data = request.form.to_dict()
    except requests.exceptions.Timeout:
        return jsonify(
            {'message': "Oops. Connection Timeout occurred. Check your internet connection", 'angle_value': None})
    except requests.exceptions.ConnectionError:
        return jsonify({'message': "Connection Error occurred. Check your internet connection", 'angle_value': None})
    except requests.exceptions.HTTPError:
        return jsonify({'message': "Http Error occurred. Check your internet connection", 'angle_value': None})
    except requests.exceptions.RequestException:
        return jsonify(
            {'message': "Request Exception occurred. make sure you followed all the steps correctly",
             'angle_value': None})

    x1 = int(request_data['x1-coord'])
    y1 = int(request_data['y1-coord'])
    x2 = int(request_data['x2-coord'])
    y2 = int(request_data['y2-coord'])
    x3 = int(request_data['x3-coord'])
    y3 = int(request_data['y3-coord'])

    pointsList.append([x1, y1])
    pointsList.append([x2, y2])
    pointsList.append([x3, y3])
    print(x1, ",", y1)
    print(x2, ",", y2)
    print(x3, ",", y3)

    if len(pointsList) == 3:
        angle_value = getAngle(pointsList)
        print("value calculated")
        return jsonify({'message': 'success', 'angle_value': str(round(angle_value,0))})
    else:
        return jsonify({'message': "Required 3 coordinates wasn't found in parameter list", 'angle_value': None})


@lets_measure_app.route('/area_estimation_polygon', methods=['POST'])
def area_perimeter_estimation_polygon():
    try:
        file = request.files['image']
    except requests.exceptions.Timeout:
        return jsonify(
            {'message': 'Oops! it client-server connection timeout occurred.',   'image': None,
             'no of object': None, 'area-polygon': None, 'perimeter-polygon': None})
    except requests.exceptions.ConnectionError:
        return jsonify(
            {'message': 'There seems to be a connection error.  Check your internet connection',
             'image': None, 'no of object': None, 'area-polygon': None, 'perimeter-polygon': None})
    except requests.exceptions.HTTPError:
        return jsonify(
            {'message': 'Http Connection Error occurred.  Check your internet connection',
             'image': None, 'no of object': None, 'area-polygon': None, 'perimeter-polygon': None})
    except requests.exceptions.RequestException:
        return jsonify({'message': 'A RequestException occurred. Check your internet connection',
                        'image': None, 'no of object': None, 'area-polygon': None, 'perimeter-polygon': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    image_canny = image_preprocessing(opencv_image)
    result_image, no_of_object, area_list, perimeter_list = area_polygon(opencv_image, image_canny)
    return_value, image2str = cv2.imencode('.jpg', result_image)
    print("area_estimation_polygon was accessed")
    image_encode = base64.b64encode(image2str).decode()
    if no_of_object > 1:
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no of object': no_of_object,
                        'area-polygon': area_list, 'perimeter-polygon': perimeter_list})
    elif no_of_object == 1:
        return jsonify({'message': 'Both ArUco and Object should be present', 'size': [w, h],
                        'image': None, 'no of object': no_of_object,
                        'area-polygon': None, 'perimeter-polygon': None})
    else:
        return jsonify({'message': 'success', 'size': [w, h], 'image': None, 'no of object': no_of_object,
                        'area-polygon': None, 'perimeter-polygon': None})


@lets_measure_app.route('/area_estimation_circle', methods=['POST'])
def area_circumference_estimation_circle():
    try:
        file = request.files['image']
    except requests.exceptions.Timeout:
        return jsonify(
            {'message': 'Oops! it client-server connection timeout occurred.',   'image': None,
             'no of object': None, 'area-circle': None, 'perimeter-circle': None})
    except requests.exceptions.ConnectionError:
        return jsonify(
            {'message': 'There seems to be a connection error.  Check your internet connection',
             'image': None, 'no of object': None, 'area-circle': None, 'perimeter-circle': None})
    except requests.exceptions.HTTPError:
        return jsonify(
            {'message': 'Http Connection Error occurred.  Check your internet connection',
             'image': None, 'no of object': None, 'area-circle': None, 'perimeter-circle': None})
    except requests.exceptions.RequestException:
        return jsonify({'message': 'A RequestException occurred. Check your internet connection',
                        'image': None, 'no of object': None, 'area-circle': None, 'perimeter-circle': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    w = image.width
    h = image.height
    image_canny = image_preprocessing(opencv_image)
    result_image, no_of_object, circle_x_y_area = area_circle(opencv_image, image_canny)
    return_value, image2str = cv2.imencode('.jpg', result_image)
    print("area_estimation_circle() was accessed")
    image_encode = base64.b64encode(image2str).decode()

    if no_of_object > 0:
        area_list = []
        perimeter_list = []
        for i in circle_x_y_area:
            area_list.append(i[3])
            perimeter_list.append(i[4])
        return jsonify({'message': 'success', 'size': [w, h], 'image': image_encode, 'no of object': no_of_object,
                        'area-circle': area_list, 'perimeter-circle': perimeter_list})
    else:
        return jsonify({'message': 'success', 'size': [w, h], 'image': None, 'no of object': no_of_object,
                        'area-circle': None, 'perimeter-circle': None})


@lets_measure_app.route('/area_estimation_irregular', methods=['POST'])
def area_perimeter_estimation_irregular():
    try:
        file = request.files['image']
    except requests.exceptions.Timeout:
        return jsonify(
            {'message': 'Oops! it client-server connection timeout occurred.',   'image': None,
             'no of object': None, 'area-irregular': None, 'perimeter-irregular': None})
    except requests.exceptions.ConnectionError:
        return jsonify(
            {'message': 'There seems to be a connection error.  Check your internet connection',
             'image': None, 'no of object': None, 'area-irregular': None, 'perimeter-irregular': None})
    except requests.exceptions.HTTPError:
        return jsonify(
            {'message': 'Http Connection Error occurred.  Check your internet connection',
             'image': None, 'no of object': None, 'area-irregular': None, 'perimeter-irregular': None})
    except requests.exceptions.RequestException:
        return jsonify(
            {'message': 'A RequestException occurred. Check your internet connection',
             'image': None, 'no of object': None, 'area-irregular': None, 'perimeter-irregular': None})

    image = Image.open(file.stream)
    opencv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    image_canny = image_preprocessing(opencv_image)
    result_image, no_of_object, area_list, perimeter_list = area_irregular(opencv_image, image_canny)
    return_value, image2str = cv2.imencode('.jpg', result_image)
    print("area_estimation_polygon was accessed")
    image_encode = base64.b64encode(image2str).decode()
    if no_of_object > 1: #more than 2 object refers to 1 object and aruco
        return jsonify({'message': 'success',   'image': image_encode, 'no of object': no_of_object,
                        'area-irregular': area_list, 'perimeter-irregular': perimeter_list})
    elif no_of_object == 1:
        return jsonify({'message': 'ArUco and object should be present!', 'image': None, 'no of object': no_of_object,
                        'area-irregular': None, 'perimeter-irregular': None})
    else:
        return jsonify({'message': 'success',   'image': None, 'no of object': no_of_object,
                        'area-irregular': None, 'perimeter-irregular': None})

if __name__ == "__main__":
    lets_measure_app.run(debug=True)
