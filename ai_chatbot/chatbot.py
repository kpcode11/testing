import fitz  # PyMuPDF
import os
import requests
import google.generativeai as genai

# Configure Google Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model_name = "gemini-1.5-flash"

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        return text
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return None

# Function to ask Gemini AI based on PDF content
def ask_gemini(question, context):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(f"Context: {context}\n\nQuestion: {question}", stream=True)
    return response

# Function to search the web using Gemini API
def search_web(query):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(f"Question: {query}", stream=True)
    return response

# Main interactive loop
print("Choose an option:")
print("1. Upload a PDF and ask questions based on its content")
print("2. Ask questions based on internet data")
print("Type 'exit' to quit.\n")

while True:
    choice = input("Enter your choice (1/2/exit): ").strip().lower()
    if choice == "exit":
        print("Goodbye!")
        break

    if choice == "1":
        pdf_path = input("Enter the path to your PDF file: ").strip()
        pdf_text = extract_text_from_pdf(pdf_path)
        if pdf_text:
            print("\nPDF successfully loaded! You can now ask questions.")
            print("Type 'back' to return to the main menu.\n")
            
            while True:
                question = input("Ask a question based on the PDF: ").strip()
                if question.lower() == "back":
                    print("Returning to the main menu...\n")
                    break
                
                response = ask_gemini(question, pdf_text)
                print("\nAnswer: ", end="")
                for chunk in response:
                    print(chunk.text, end="")
                print("\n")
    elif choice == "2":
        print("You can now ask questions based on internet data.")
        print("Type 'back' to return to the main menu.\n")
        
        while True:
            question = input("Ask a question: ").strip()
            if question.lower() == "back":
                print("Returning to the main menu...\n")
                break
                
            response = search_web(question)
            print("\nAnswer: ", end="")
            for chunk in response:
                print(chunk.text, end="")
            print("\n")
    else:
        print("Invalid choice. Please enter '1', '2', or 'exit'.\n")