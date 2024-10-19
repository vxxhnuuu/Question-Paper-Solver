import os
import html
from flask import Flask, request, render_template, jsonify
from PIL import Image  # Ensure you have Pillow installed for image handling
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

# Constants for API configuration
API_KEY = os.getenv("API_KEY")  # Load the API key from environment variables
CUSTOM_PROMPT = "Solve the given questions and print both question and answer to the question:\n\n"

def configure_api():
    if not API_KEY:
        raise ValueError("API key is not set.")
    genai.configure(api_key=API_KEY)

def generate_image_response(text_prompt, image_path):
    # Configure API
    configure_api()

    # Combine the custom prompt with the user's text input
    prompt_full = f"{CUSTOM_PROMPT} {text_prompt}"
    
    try:
        # Load the image using PIL
        image = Image.open(image_path)

        # Initialize the model (replace 'gemini-1.5-flash' with your actual model identifier)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Send the combined text prompt and image to the model
        response = model.generate_content([prompt_full, image])
        
        if response:
            # Decode HTML entities and clean up any extra symbols in the response
            decoded_response = html.unescape(response.text)
            cleaned_response = decoded_response.replace('*', '').replace('**', '')
            return cleaned_response.strip()  # Ensure no leading or trailing whitespace
        
        return "No response generated."
    
    except Exception as e:
        return f"Error: {str(e)}"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            
            prompt = "Your custom prompt here."  # Adjust as necessary
            
            # Generate the response using the Gemini API
            response = generate_image_response(prompt, file_path)
            
            return render_template('result.html', response=response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        configure_api()
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        app.run(debug=True)
    except Exception as e:
        print(f"Configuration error: {e}")
