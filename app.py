from flask import Flask, request, jsonify, render_template, make_response
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import jwt
import datetime
from functools import wraps
import gc
# GPU Utilization
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2000)]) # 2000MB=2GB
    except RuntimeError as e:
        print(e)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'
class_names = ["0","1","2","3","4","5","6","7","8","9"]
input_shape = (28,28)
model = keras.models.load_model('mnist_nn.h5')

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#
#         # token = flask.request.args.get('token') # http://127.0.0.1:5000/route?token=s1234fr5tg-gyt
#
#         if not auth or not auth.token:
#             return jsonify({'message' : 'Token is missing!'}), 401
#
#         token = auth.token
#
#         try:
#             data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message' : 'Token has expired!'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message' : 'Token is invalid!'}), 401
#
#         return f(*args, **kwargs)
#     return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') # http://127.0.0.1:5000/route?token=s1234fr5tg-gyt

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try:
            data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)
    return decorated

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

@app.route('/predict', methods=['GET','POST'])
@token_required
def predict():
    if request.method == 'GET':
        return render_template('upload.html')
    # ensure an image was properly uploaded to our endpoint
    if not request.files.get("image"):
        return jsonify({'message' : "Image not recevied!"}), 403
    if request.method =='POST':

        image_file = request.files['image']
        image_data = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        print(image_data.shape)
        print(type(image_data))


        image = preprocess_image(image_data, input_shape)
        cls = model.predict(image)
        cls = class_names[np.argmax(cls)]
        return render_template('class.html', cls=cls)

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)},app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

