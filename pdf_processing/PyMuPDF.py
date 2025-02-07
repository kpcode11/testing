import fitz  # PyMuPDF
import os
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

# Function to start a new chat
def start_chat(history=None):
    model = genai.GenerativeModel(model_name)
    if history is None:
        history = [{"role": "user", "parts": "Hello"}, {"role": "model", "parts": "Great to meet you. What would you like to know?"}]
    chat = model.start_chat(history=history)
    return chat, history

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
            
            history = [
                {"role": "user", "parts": "Please use the following content to answer questions: "},
                {"role": "model", "parts": pdf_text}
            ]  # Initialize chat history with PDF content
            chat, history = start_chat(history)

            while True:
                question = input("Ask a question based on the PDF: ").strip()
                if question.lower() == "back":
                    print("Returning to the main menu...\n")
                    break

                response = chat.send_message(question)
                print("\nAnswer:", response.text)
                history.append({"role": "user", "parts": question})
                history.append({"role": "model", "parts": response.text})
    elif choice == "2":
        print("You can now ask questions based on internet data.")
        print("Type 'back' to return to the main menu.\n")
        
        history = [{"role": "user", "parts": "Hello"}, {"role": "model", "parts": "Great to meet you. What would you like to know?"}]  # Initialize chat history for internet data
        chat, history = start_chat(history)

        while True:
            question = input("Ask a question: ").strip()
            if question.lower() == "back":
                print("Returning to the main menu...\n")
                break

            response = chat.send_message(question)
            print("\nAnswer:", response.text)
            history.append({"role": "user", "parts": question})
            history.append({"role": "model", "parts": response.text})
    else:
        print("Invalid choice. Please enter '1', '2', or 'exit'.\n")
