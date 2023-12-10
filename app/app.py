from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageFilter
# import cv2
import numpy as np
# import tensorflow as tf
from tensorflow import keras
from flask_basicauth import BasicAuth
# import base64
# import psycopg2
import mysql.connector
# import gc
import io
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# GPU Utilization
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         tf.config.experimental.set_virtual_device_configuration(gpus[0], [
#             tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1000)])  # 2000MB=2GB
#     except RuntimeError as e:
#         print(e)
app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = "dam"
app.config["BASIC_AUTH_PASSWORD"] = "damp"

basic_auth = BasicAuth(app)
class_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
input_shape = (28, 28)
model = keras.models.load_model('mnist_nn.h5')


def write_to_employee_data(image: bytearray, prediction: str):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'digit'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "INSERT INTO classification_data (image, prediction) VALUES (%s, %s)"
    values = (image, prediction)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()


def preprocess_image(image, input_size=(28, 28)):

    # Convert the image to grayscale
    gray = image.convert("L")

    # Resize to the input size expected by your model
    resized_img = gray.resize(input_size, Image.LANCZOS)

    # Convert to NumPy array and normalize pixel values to be in the range [0, 1]
    normalized_img = np.array(resized_img) / 255.0

    # Add batch dimension
    input_tensor = np.expand_dims(normalized_img, axis=0)

    return input_tensor


@app.route('/predict', methods=['GET', 'POST'])
@basic_auth.required
def predict():
    if request.method == 'GET':
        return render_template('upload.html')
    # ensure an image was properly uploaded to our endpoint
    if not request.files.get("image"):
        return jsonify({'message': "Image not received!"}), 403
    if request.method == 'POST':

        file = request.files['image']
        # Read the binary image data
        file_bin = file.read()
        image = Image.open(io.BytesIO(file_bin))

        # Convert binary data to bytearray # to store in DB
        byte_array = bytearray(file_bin)

        # print(image_data.shape)
        # print(type(image_data))

        image = preprocess_image(image, input_shape)
        cls = model.predict(image)
        cls = class_names[np.argmax(cls)]
        write_to_employee_data(byte_array,cls)
        return render_template('class.html', cls=cls)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
