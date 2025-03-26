import PyPDF2
from docx import Document
import win32com.client
import pytesseract
from PIL import Image
import re
import fitz  # PyMuPDF
import io

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    
    pdf_file = fitz.open(pdf_path)
    for page_index in range(len(pdf_file)):

        # get the page itself
        page = pdf_file.load_page(page_index)  # load the page
        image_list = page.get_images(full=True)
        if image_list:
            for image_index, img in enumerate(image_list, start=1):
                # get the XREF of the image
                xref = img[0]

                # extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]

                # get the image extension
                image_ext = base_image["ext"]

                # save the image
                image_name = f"image{page_index+1}_{image_index}.{image_ext}"
                with open(image_name, "wb") as image_file:
                    image_file.write(image_bytes)
                text += extract_text_from_jpg(image_file)        
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_doc(doc_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(doc_path)
    text = doc.Content.Text
    doc.Close(False)
    word.Quit()
    return text

def extract_text_from_jpg(jpg_path):
    text = pytesseract.image_to_string(Image.open(jpg_path))
    return text
    

def preprocess_text(text):
    # Convert text to lowercase
    # text = text.lower()
    # Remove email addresses
    # text = re.sub(r'\S+@\S+', '', text)
    # Remove URLs
    # text = re.sub(r'http\S+|www\S+', '', text)
    # Remove special characters and numbers
    # text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.doc'):
        text = extract_text_from_doc(file_path)
    elif file_path.endswith('.jpg'):
        text = extract_text_from_jpg(file_path)
    else:
        raise ValueError("Unsupported file format")
    # Print the extracted text before preprocessing
    # print("Extracted Text Before Preprocessing:")
    # print(text)
    # Preprocess the extracted text
    # print("Extracted Text After Preprocessing:")
    text = preprocess_text(text)
    return text

# Sample usage
pdf_path = "E:\\hackathon-emailrouting\\Sample_PDF.pdf"
docx_path = "E:\\hackathon-emailrouting\\Sample_DOCX.docx"
doc_path = "E:\\hackathon-emailrouting\\Sample_DOC.doc"
jpg_path = "E:\\hackathon-emailrouting\\Sample_JPG.jpg"

print("PDF Content:")
print(extract_text(pdf_path))

print("\nDOCX Content:")
print(extract_text(docx_path))

print("\nJPG Content:")
print(extract_text(jpg_path))

print("\nDOC Content:")
print(extract_text(doc_path))
