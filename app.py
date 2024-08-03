import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from google.cloud import vision
from google.oauth2 import service_account
import google.generativeai as genai
from flask_cors import CORS

# Configure the Google Cloud Vision API client
def configure_vision_api():
    credentials = service_account.Credentials.from_service_account_file(
        r'C:\Users\vishn\Desktop\Question Paper Solver\just-site-429414-d5-a3d60715a33a.json'  # Replace with the path to your JSON key file
    )
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client

# Configure the Gemini API
def configure_api():
    genai.configure(api_key="AIzaSyAkeGOaW3tXIqjVghmT3CwvY2D8FgEXI9Y")  # Replace with your actual API key

def generate_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")  # Replace with your actual model identifier
    response = model.generate_content(prompt)
    return response.text if response else "No response generated"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            text = extract_text_from_image(file_path)
            prompt = f"Solve the given questions and print both question and answer to the question:\n\n{text}"
            response = generate_response(prompt)
            
            return render_template('result.html', extracted_text=text, response=response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_text_from_image(image_path):
    client = configure_vision_api()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return ""

if __name__ == '__main__':
    configure_api()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
