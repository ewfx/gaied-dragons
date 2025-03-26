import os
from email import policy
from email.parser import BytesParser
import extract_msg

def extract_eml_content(eml_path, output_dir):
    combined_content = ""

    # Parse the .eml file
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    # Extract email content
    def extract_email_content(msg, level=0):
        nonlocal combined_content
        email_content = {
            "subject": msg['subject'],
            "from": msg['from'],
            "to": msg['to'],
            "date": msg['date'],
            "body": msg.get_body(preferencelist=('plain', 'html')).get_content()
        }
        
        # Print email content
        # print(f"Email Content (Level {level}):")
        for key, value in email_content.items():
            # print(f"{key}: {value}")
            combined_content += f"{key}: {value}\n"
        
        # Extract attachments
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                # print(f"Attachment saved: {filepath}")
        
        # Recursively extract nested emails
        for part in msg.iter_parts():
            if part.get_content_type() == "message/rfc822":
                nested_msg = part.get_payload(0)
                extract_email_content(nested_msg, level + 1)
    
    extract_email_content(msg)
    return combined_content

def extract_msg_content(msg_path, output_dir):
    # Parse the .msg file
    msg = extract_msg.Message(msg_path)
    msg.save(output_dir)
    
    # Extract email content
    email_content = {
        "subject": msg.subject,
        "from": msg.sender,
        "to": msg.to,
        "date": msg.date,
        "body": msg.body
    }
    
    # Print email content
    # print("Email Content:")
    for key, value in email_content.items():
        # print(f"{key}: {value}")
        pass
    
    # Extract attachments
    for attachment in msg.attachments:
        filepath = os.path.join(output_dir, attachment.longFilename)
        with open(filepath, "wb") as f:
            f.write(attachment.data)
        # print(f"Attachment saved: {filepath}")

# Example usage
if __name__ == "__main__":
    eml_path = "E:\\hackathon-emailrouting\\Sample_EML_Multiple_Mail.eml"  # Replace with the path to your .eml file
    msg_path = "E:\\hackathon-emailrouting\\Sample_MSG_With_DOCX.msg"  # Replace with the path to your .msg file
    output_dir = "E:\\hackathon-emailrouting\\output_attachments"  # Replace with the path to your output directory
    
    # Extract content from .eml file and print it
    eml_content = extract_eml_content(eml_path, output_dir)
    # print("Extracted Email Content:")
    # print(eml_content)
    
    # Extract content from .msg file
    # extract_msg_content(msg_path, output_dir)