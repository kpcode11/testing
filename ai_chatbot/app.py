from flask import Flask, request, jsonify
import os
import PyPDF2
import fitz  # PyMuPDF
import google.generativeai as genai

app = Flask(__name__)

# Access the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    raise ValueError("API key not set. Please set the GOOGLE_API_KEY environment variable.")

# Configure Google Gemini with the API key
genai.configure(api_key=api_key)

stored_text = ""

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# @app.route("/upload", methods=["POST"])
# def upload_pdf():
#     """Handle PDF uploads and extract text."""
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "Empty filename"}), 400

#     file_path = os.path.join("uploads", file.filename)
#     os.makedirs("uploads", exist_ok=True)
#     file.save(file_path)

#     extracted_text = extract_text_from_pdf(file_path)
#     return jsonify({"text": extracted_text})

@app.route('/upload', methods=['POST'])
def upload_file():
    global stored_text  # Use the global variable to store text

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Extract text from the PDF
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Store the extracted text in memory
    stored_text = text

    return jsonify({"message": "File uploaded successfully", "extracted_text": stored_text[:200]})  # Send part of the text for confirmation



@app.route('/ask', methods=['POST'])
def ask_question():
    global stored_text  # Use the stored text from the PDF

    if not stored_text:
        return jsonify({"error": "No document uploaded yet"}), 400

    question = request.json.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Use a simple text search (or AI model) to find an answer based on the stored text
    answer = search_text_for_answer(question, stored_text)
    
    return jsonify({"answer": answer})

def search_text_for_answer(question, text):
    # A very simple way to search for the answer in the text
    if question.lower() in text.lower():
        return "I found something related to your question."
    else:
        return "Sorry, I couldn't find an answer."

if __name__ == "__main__":
    app.run(debug=True)
