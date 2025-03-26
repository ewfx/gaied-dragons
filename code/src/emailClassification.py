import os
from emailExtractEML import extract_eml_content
from emailExtract import extract_text
from emailEMLPreprocess import clean_text
from groqLLM import classify_query  # Import the classify_query function

def classify_email(eml_path, output_dir):
    # Extract content from .eml file
    eml_content = extract_eml_content(eml_path, output_dir)
    print(eml_content)
    # Preprocess the extracted email content
    preprocessed_content = clean_text(eml_content)
    print(preprocessed_content)

    # Check for attachments and process them
    attachments_info = ""
    for filename in os.listdir(output_dir):
        if filename.endswith(('.pdf', '.docx', '.doc', '.jpg')):
            file_path = os.path.join(output_dir, filename)
            attachment_text = extract_text(file_path)
            attachments_info += f"\nAttachment ({filename}):\n{attachment_text}\n"
    
    # Combine email content and attachments info
    combined_content = preprocessed_content + attachments_info
    # check whether it is duplicate content or not
    # Call the LLM for classification
    response = classify_query(combined_content)
    
    # Print the response
    print("User Query:", combined_content)
    print("LLM Response:", response)

# Example usage
if __name__ == "__main__":
    eml_path = "E:\\hackathon-emailrouting\\Sample_EML_With_DOCX.eml"  # Replace with the path to your .eml file
    output_dir = "E:\\hackathon-emailrouting\\output_attachments"  # Replace with the path to your output directory
    
    classify_email(eml_path, output_dir)