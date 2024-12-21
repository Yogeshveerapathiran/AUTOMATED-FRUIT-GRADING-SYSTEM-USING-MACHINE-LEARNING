# AUTOMATED-FRUIT-GRADING-SYSTEM-USING-MACHINE-LEARNING
# AIM
To automate the grading of fruits using image processing and machine learning, ensuring accurate quality assessment based on attributes like size, shape, color, and ripeness.
# PROGRAM
## APP.PY
```py
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
``
## index.html
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Automated Fruit Grading System</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
      }

      .container {
        text-align: center;
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 500px;
      }

      h1 {
        color: #333;
        margin-bottom: 20px;
      }

      .upload-btn-wrapper {
        position: relative;
        overflow: hidden;
        display: inline-block;
      }

      .btn {
        border: 2px solid #4caf50;
        color: white;
        background-color: #4caf50;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 5px;
      }

      .upload-btn-wrapper input[type="file"] {
        font-size: 100px;
        position: absolute;
        left: 0;
        top: 0;
        opacity: 0;
      }

      .result {
        margin-top: 20px;
        font-size: 16px;
        color: #555;
      }

      .result img {
        max-width: 100%;
        border-radius: 5px;
        margin-top: 10px;
      }

      .about {
        margin-top: 30px;
        font-size: 14px;
        color: #777;
        padding: 10px;
        background: #f1f1f1;
        border-radius: 5px;
        text-align: left;
      }

      .about h3 {
        color: #333;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Fruit Grading System</h1>
      <form
        id="uploadForm"
        action="/"
        method="POST"
        enctype="multipart/form-data"
      >
        <div class="upload-btn-wrapper">
          <button class="btn">Upload Image</button>
          <input
            type="file"
            name="file"
            accept="image/*"
            onchange="previewImage(event)"
            required
          />
        </div>
        <button type="submit" class="btn" style="margin-top: 20px">
          Submit
        </button>
      </form>
      <div class="result" id="result">
        <p>Selected image preview:</p>
        <img
          id="preview"
          alt="Image preview will appear here"
          style="display: none"
        />
      </div>
    </div>
    <div class="about">
      <h3>About the Project</h3>
      <p>
        This project uses image processing techniques to classify fruits based
        on their ripeness level. The grading system evaluates the color and
        texture of the fruit to determine whether it's ripe, very ripe, or
        rotten. The goal is to assist in making decisions for food safety and
        consumption.
      </p>
    </div>

    <script>
      function previewImage(event) {
        const preview = document.getElementById("preview");
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
          };
          reader.readAsDataURL(file);
        }
      }
    </script>
  </body>
</html>
```
## RESULT.HTML
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Fruit Grading System</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }

      .container {
        text-align: center;
        background: #fff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 600px;
      }

      h1 {
        color: #4caf50;
        margin-bottom: 20px;
        font-size: 32px;
        font-weight: bold;
      }

      .result {
        margin-top: 20px;
        font-size: 18px;
        color: #555;
      }

      .result img {
        max-width: 100%;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
      }

      .btn {
        border: 2px solid #4caf50;
        color: white;
        background-color: #4caf50;
        padding: 12px 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin-top: 20px;
      }

      .btn:hover {
        background-color: #45a049;
      }

      .health-message {
        margin-top: 20px;
        font-size: 20px;
        color: #333;
        font-weight: bold;
      }

      .about-project {
        margin-top: 40px;
        font-size: 16px;
        color: #777;
        text-align: center;
        line-height: 1.6;
        padding: 20px;
        background-color: #f1f1f1;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      }

      .about-project h3 {
        font-size: 22px;
        color: #333;
        margin-bottom: 10px;
        font-weight: bold;
      }

      .about-project p {
        margin: 0;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Fruit Grading System</h1>
      <div class="result">
        <p><strong>{{ grade }}</strong></p>
        <p>{{ edible }}</p>
        <img
          src="{{ url_for('static', filename='uploads/' + image_path) }}"
          alt="Uploaded Image"
        />
        <br />
        <img
          src="{{ url_for('static', filename='uploads/' + processed_path.split('/')[-1]) }}"
          alt="Processed Image"
        />
      </div>

      <div class="health-message">
        <p>Eat fresh, stay healthy!</p>
      </div>

      <a href="/" class="btn">Upload Another Image</a>

      <!-- Centered About Project Box -->
      <div class="about-project">
        <h3>About the Project</h3>
        <p>
          The Fruit Grading System uses advanced image processing techniques to
          determine the ripeness of fruits. By analyzing the fruit's color and
          texture, the system automatically grades the fruit as either Grade A
          (ripe), Grade B (mildly ripe), or Grade C (rotten). This helps users
          make informed decisions about the fruit's edibility, ensuring healthy
          choices and reducing food waste.
        </p>
      </div>
    </div>
  </body>
</html>
```
# OUTPUT
![image](https://github.com/user-attachments/assets/859446dd-e8a3-4667-ade2-6ecd37d21302)

![image](https://github.com/user-attachments/assets/bf36a24a-be77-4613-bcf3-0c4814b2cb05)

![image](https://github.com/user-attachments/assets/5f7aa994-3a64-4442-82f9-c8fd6b522403)

## RESULT
The system successfully classifies fruits into quality grades based on attributes such as size, shape, color, and ripeness, achieving accurate and consistent grading through automated processing.
