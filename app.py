import os
from flask import Flask, request, render_template, jsonify
from google.cloud import vision
from google.oauth2 import service_account
import google.generativeai as genai
from flask_cors import CORS

# Configure the Google Cloud Vision API client
def configure_vision_api():
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client

# Configure the Gemini API
def configure_api():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    genai.configure(api_key=api_key)

def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Replace with your actual model identifier
        response = model.generate_content(prompt)
        return response.text if response else "No response generated"
    except Exception as e:
        return str(e)

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
    try:
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
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    try:
        configure_api()
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        app.run(debug=True)
    except Exception as e:
        print(f"Configuration error: {e}")
