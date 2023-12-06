from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import gc
# GPU Utilization
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2000)])
    except RuntimeError as e:
        print(e)
app = Flask(__name__)
class_names = ["0","1","2","3","4","5","6","7","8","9"]
input_shape = (28,28)
model = keras.models.load_model('mnist_nn.h5')

def preprocess_image(image, input_size = (28, 28)):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    # Thresholding
    thresh = cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY_INV)[1]
    # Resize to the input size expected by your model
    resized_img = cv2.resize(thresh, input_size, interpolation=cv2.INTER_AREA)
    # Normalize pixel values to be in the range [0, 1]
    normalized_img = resized_img/ 255.0
    # Add batch dimension
    input_tensor = np.expand_dims(normalized_img, axis=0)
    # input_tensor = normalized_img
    return input_tensor

@app.route('/predict', methods=['POST'])
def predict():
    # ensure an image was properly uploaded to our endpoint
    if not request.files.get("image"):
        return jsonify({'message' : "Image not recevied!"}), 403
    image_file = request.files['image']
    image_data = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    print(image_data.shape)
    print(type(image_data))


    image = preprocess_image(image_data, input_shape)
    cl = model.predict(image)
    return class_names[np.argmax(cl)]

if __name__ == '__main__':
    app.run(host='0.0.0.0')

