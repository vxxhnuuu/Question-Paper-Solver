# Question Paper Solver using LLM

## Overview

This project is a web application that utilizes a Large Language Model (LLM) to solve question papers by extracting text from uploaded images and generating answers based on the extracted content. The application leverages the Google Gemini API for text processing and response generation, providing users with an intuitive interface to upload their question papers and receive solutions.

## Features

- **Image Upload**: Users can upload images of question papers in various formats.
- **Text Extraction**: The application extracts text from images using the Google Gemini API.
- **Answer Generation**: Answers to the extracted questions are generated using the LLM, ensuring accurate and relevant responses.
- **User-Friendly Interface**: Simple and clean interface built with Flask and HTML/CSS.

## Technologies Used

- **Python**: The main programming language for backend development.
- **Flask**: A micro web framework for building the web application.
- **Pillow**: A Python Imaging Library (PIL) fork used for image handling.
- **Google Gemini API**: Used for text extraction and response generation.
- **dotenv**: For loading environment variables from a .env file.
- **HTML/CSS**: For frontend development.

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/question-paper-solver.git
   cd question-paper-solver
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:

   - Create a .env file in the root directory of your project.
   - Add your Google Gemini API key to the .env file:

     ```
     API_KEY=your_actual_api_key_here
     ```

5. **Run the Application**:

   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open your web browser and go to http://127.0.0.1:5000/ to access the application.

## Usage

1. On the main page, upload an image of your question paper.
2. Click the "Submit" button to process the image.
3. The application will extract text from the image and generate answers for the questions.
4. The results will be displayed on a new page.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find bugs, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Google Cloud](https://cloud.google.com/) for the Gemini API.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Pillow](https://python-pillow.org/) for image handling.

## Contact

For any questions or inquiries, feel free to reach out:

- Vishnu Dathan - vishnud0098@gmail.com
- GitHub: vxxhnuuu
