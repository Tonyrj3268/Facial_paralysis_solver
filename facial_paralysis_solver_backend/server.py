
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import ganimation_IR_use
from PIL import Image
import base64
import numpy as np
import cv2
from face_landmark import facemesh
import json

import matplotlib.pyplot as plt

app = Flask(__name__)
cors = CORS(app, origins=['http://127.0.0.1:5173'])
app.config['CORS_HEADERS'] = 'Content-Type'

def prefixLandmark(detections):
    numbers = []
    # Use a for loop to add the numbers from 0 to 467 to the list
    for i in range(0, 468, 1):
        numbers.append(i)
    silhouette= [
    10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109]

    lipsUpperOuter= [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
    lipsLowerOuter= [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
    lipsUpperInner= [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
    lipsLowerInner= [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

    rightEyeUpper0= [246, 161, 160, 159, 158, 157, 173]
    rightEyeLower0= [33, 7, 163, 144, 145, 153, 154, 155, 133]
    rightEyeUpper1= [247, 30, 29, 27, 28, 56, 190]
    rightEyeLower1= [130, 25, 110, 24, 23, 22, 26, 112, 243]
    

    rightEyebrowUpper= [156, 70, 63, 105, 66, 107, 55, 193]
    rightEyebrowLower= [35, 124, 46, 53, 52, 65]

    leftEyeUpper0= [466, 388, 387, 386, 385, 384, 398]
    leftEyeLower0= [263, 249, 390, 373, 374, 380, 381, 382, 362]
    leftEyeUpper1= [467, 260, 259, 257, 258, 286, 414]
    leftEyeLower1= [359, 255, 339, 254, 253, 252, 256, 341, 463]
    

    leftEyebrowUpper= [383, 300, 293, 334, 296, 336, 285, 417]
    leftEyebrowLower= [265, 353, 276, 283, 282, 295]
    noseTip= [1]
    noseBottom= [2]
    noseRightCorner= [98]
    noseLeftCorner= [327]

    removed_index = silhouette  + lipsUpperOuter + lipsLowerOuter + lipsUpperInner + lipsLowerInner + rightEyeUpper0 + rightEyeLower0 + rightEyeUpper1 + rightEyeLower1 + rightEyebrowUpper + rightEyebrowLower + leftEyeUpper0 + leftEyeLower0 + leftEyeUpper1 + leftEyeLower1 + leftEyebrowUpper + leftEyebrowLower
    removed_index = removed_index + noseTip + noseBottom + noseRightCorner + noseLeftCorner
    numbers = [i for i in numbers if i not in removed_index]
    detections = np.delete(detections,numbers,axis = 0)
    x, y = detections[:, 0], detections[:, 1]
   
    x = np.ndarray.tolist(x)
    y = np.ndarray.tolist(y)
    return x,y


@app.route('/upload', methods=['POST'])
def upload_image():
    img = request.form['image']
    # Remove the "data:image/[image_format];base64," prefix from the image data
    image_data = img.split(",")[1]
    image_data = bytes(image_data, "utf-8")
    # Decode the base64 image data and store it in a NumPy array
    image_array = np.frombuffer(base64.decodebytes(image_data), dtype=np.uint8)
    print(image_array.shape)
    
    img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (128,128))
    ga = ganimation_IR_use.ganimation(img)
    result = ga.produce_pics()

    info = {}
    for i in range(16):
        path = "./result/hannibal_{}.jpg".format(i)
       
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,(192,192))
        face = facemesh.facemesh()
        detections = face.produce(img)
        detections = detections.reshape(-1, 3)
        x, y = prefixLandmark(detections)
        print('標記landmark完成{}/16'.format(i+1))
        info['x{}'.format(i+1)] = x
        info['y{}'.format(i+1)] = y

        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        info['image{}'.format(i+1)] = encoded_string.decode()
    return jsonify(info)


@app.route('/compare', methods=['POST'])
def compare_lanmark():
    img = request.form['image']
    # Remove the "data:image/[image_format];base64," prefix from the image data
    image_data = img.split(",")[1]
    image_data = bytes(image_data, "utf-8")
    # Decode the base64 image data and store it in a NumPy array
    image_array = np.frombuffer(base64.decodebytes(image_data), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (192,192))
    face = facemesh.facemesh()
    detections = face.produce(img)
    detections = detections.reshape(-1, 3)
    x, y = prefixLandmark(detections)
    newLandmark = {}
    newLandmark['x1'] = x
    newLandmark['y1'] = y
    
    # newLandmark = jsonify(newLandmark)
    # print(newLandmark)
    landmark = request.form['landmark']
    landmark = json.loads(landmark)
    print(np.array(landmark['x1']))

    error = np.sqrt(sum((np.array(landmark['x1'])-np.array(newLandmark['x1']))**2)+sum
    ((np.array(landmark['y1'])-np.array(newLandmark['y1']))**2))
    error=error*-1 + 100
    newLandmark.update({"score":error})    

    return jsonify(newLandmark)

if __name__ == '__main__':
    app.run()