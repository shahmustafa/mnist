from flask import FLask, request, jsonify
import cv2
import numpy as np
from tensorflow import keras
import gc

app = FLask(__name__)
class_names = ["0","1","2","3","4","5","6","7","8","9"]
model = keras.models.load_model('mnist_nn.h5')

def prepare_img(image, shape):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    b_img = cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY_INV)[1]
    b_img = cv2.resize(b_img, shape)
    b_img = b_img / 255
    return b_img
@app.route('/predict', methods=['POST'])
def predict():
    pass

