# FLASK_APP=main.py FLASK_ENV=development flask run
from flask import Flask, request, make_response
from werkzeug.datastructures import FileStorage
import cv2
import numpy as np


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/firma', methods=('POST', 'GET'))
def signature():
    if request.method == 'POST':
        img_stream: FileStorage = request.files['img']
        img_bytes: bytes = img_stream.stream.read()

        img_arr = np.frombuffer(img_bytes, np.uint8)
        img: np.ndarray = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)

        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # plt.show()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        bin_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 55, 4)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(bin_img, kernel, iterations=1)

        rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        rgba[:, :, 3] = cv2.bitwise_and(rgba[:, :, 3], mask)

        ret = cv2.imencode('.png', rgba)[1].tobytes()

        return make_response(ret)
    return 'POST request plz'


if __name__ == '__main__':
    app.run()
