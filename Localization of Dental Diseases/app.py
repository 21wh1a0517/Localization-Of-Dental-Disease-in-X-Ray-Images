# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from werkzeug.utils import secure_filename
# import os
# import base64
# import secrets
# from ultralytics import YOLO
# from PIL import Image, ImageDraw, ImageFont
# import io

# app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)
# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load the YOLO model
# model = YOLO("dental_model.pt")

# # Dummy credentials
# USERNAME = "admin"
# PASSWORD = "12345"

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == USERNAME and password == PASSWORD:
#             session['logged_in'] = True
#             return redirect(url_for('home'))
#         else:
#             return render_template('index.html', error='Invalid Credentials')
#     return render_template('index.html')

# @app.route('/home')
# def home():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     return render_template('home.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return redirect(url_for('home'))
#     file = request.files['file']
#     if file.filename == '':
#         return redirect(url_for('home'))
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
#     filename = secure_filename(file.filename)
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(filepath)
#     session['uploaded_file'] = filename
#     return redirect(url_for('detect'))

# @app.route('/detect')
# def detect():
#     if 'uploaded_file' not in session:
#         return redirect(url_for('home'))
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], session['uploaded_file'])
#     image = Image.open(filepath).convert("RGB")
#     results = model.predict(image)
#     result = results[0]

#     draw = ImageDraw.Draw(image)
#     try:
#         font = ImageFont.truetype("static/arial.ttf", 20)
#     except IOError:
#         font = ImageFont.load_default()

#     detections = []
#     for idx, box in enumerate(result.boxes, start=1):
#         x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
#         class_id = int(box.cls[0].item())
#         prob = round(box.conf[0].item(), 2)
#         prob_percentage = f"{prob * 100:.2f}%"

#         # Draw only the serial number on the image
#         draw.rectangle([(x1, y1), (x2, y2)], outline="green", width=4)
#         draw.text((x1 + 2, y1 - 20), str(idx), fill="white", font=font)

#         # Full detail below image
#         detections.append({
#             # "serial": idx,
#             "class": result.names[class_id],
#             "confidence": prob_percentage
#         })

#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)
#     encoded_img = base64.b64encode(img_byte_arr.read()).decode('utf-8')

#     return render_template('result.html', image_data=encoded_img, detections=detections)

# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import base64
import secrets
from PIL import Image
from model import predict_image

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy credentials
USERNAME = "admin"
PASSWORD = "12345"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('index.html', error='Invalid Credentials')
    return render_template('index.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    session['uploaded_file'] = filename
    return redirect(url_for('detect'))

@app.route('/detect')
def detect():
    if 'uploaded_file' not in session:
        return redirect(url_for('home'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], session['uploaded_file'])
    image_data, detections = predict_image(filepath)
    return render_template('result.html', image_data=image_data, detections=detections)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
