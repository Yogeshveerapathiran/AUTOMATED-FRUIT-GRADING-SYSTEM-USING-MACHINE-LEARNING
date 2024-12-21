from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simple grading logic based on color analysis
def determine_grade(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Calculate the mean value of the Hue channel
    mean_hue = cv2.mean(hsv)[0]

    # Simple grading logic based on hue range
    if mean_hue < 30:
        grade = "Grade: C (Rotten)"
        edible = "Please do not eat this fruit. It is rotten."
    elif 30 <= mean_hue < 60:
        grade = "Grade: B (Ripe)"
        edible = "This fruit is recommended for eating."
    else:
        grade = "Grade: A (Very Ripe)"
        edible = "This fruit is recommended for eating."

    return grade, edible

# Apply grayscale and binary thresholding
def process_grayscale_threshold(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_image.png')
    cv2.imwrite(processed_path, binary)
    return processed_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process image and determine grade
            processed_path = process_grayscale_threshold(file_path)
            grade, edible = determine_grade(file_path)

            return render_template('result.html', grade=grade, edible=edible, image_path=filename, processed_path=processed_path)
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
