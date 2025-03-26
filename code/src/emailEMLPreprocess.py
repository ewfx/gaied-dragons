import re

def clean_text(input_text):
    if not input_text:
        return input_text
    
    # Extract and format the header
    header_pattern = re.search(r'subject: (.*)\nfrom: (.*) <(.*)>\nto: (.*) <(.*)>\ndate: (.*)', input_text, re.IGNORECASE)
    
    if header_pattern:
        subject = header_pattern.group(1).strip()
        from_email = header_pattern.group(3).strip()
        to_email = header_pattern.group(5).strip()
        date = header_pattern.group(6).strip()
        
        formatted_header = f"Date : {date}\nSubject: {subject} from {from_email} to {to_email}\n"
    else:
        formatted_header = ""
    
    # Remove the header from the input text
    input_text = re.sub(r'subject: .*?\nfrom: .*?\nto: .*?\ndate: .*?\nbody:', '', input_text, flags=re.IGNORECASE | re.DOTALL)
    
    # Format inline date and email from 'On Sat, ... wrote:' lines
    input_text = re.sub(r'On (.*) at .*? ([^ ]+@[^ ]+) wrote:', lambda m: f"Date {m.group(1)} from {m.group(2).replace('@', '').replace('.', '')}", input_text)
    
    # Remove all special characters except spaces using regex for the rest of the content
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', input_text)
    
    # Replace multiple spaces with a single space and strip leading/trailing spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Ensure date and email are on the same line
    cleaned = re.sub(r'(Date .*? from [^ ]+)', r'\1', cleaned)
    
    # Add line breaks between different sections
    cleaned = re.sub(r'(Date .*? from [^ ]+)', r'\n\n\1\n\n', cleaned)
    
    # Remove the "Thanks/Regards" section at the end of the email content
    cleaned = re.sub(r'(Thank you for your prompt support|Sincerely|Regards|Thanks).*', '', cleaned, flags=re.IGNORECASE).strip()
    
    return formatted_header + '\n' + cleaned

# Example usage
input_text = """
  subject: Re: Urgent: Unauthorized Transaction on My Account
from: Rishi Prasad <rishiprasad543@gmail.com>
to: Rishi <genmailandrounting@gmail.com>
date: Sat, 22 Mar 2025 23:25:40 +0530
body: Dear ABC International Bank Support Team,

I am following up on my report regarding the unauthorized transaction of
$5,000 USD on March 18, 2025, from my account (Account Number: 1234567890).

Could you please provide an update on the investigation? I would appreciate
any information regarding the progress or any further steps I need to take.

Please feel free to contact me at +1 (123) 456-7890 or johndoe@example.com.

Thank you for your assistance.

Sincerely,

John Doe

123 Maple Street

Cityville, Countryland

+1 (123) 456-7890

johndoe@example.com


On Sat, Mar 22, 2025 at 11:24 PM Rishi <genmailandrounting@gmail.com> wrote:

> Hi John,
>
> Sorry for the inconvenience and we have raised your concern with a
> specific team. We are working on high priority for your issue.
>
> Thanks,
> ABC support team
>
> On Sat, Mar 22, 2025 at 11:08 PM Rishi Prasad <rishiprasad543@gmail.com>
> wrote:
>
>> Dear ABC International Bank Support Team,
>>
>> I am writing to report an unauthorized transaction on my account. I
>> recently discovered that my account with ABC International Bank, associated
>> with the name John Doe, has been compromised. An amount has been debited
>> without my authorization.
>>
>> Details of the account are as follows:
>>
>>    -
>>
>>    Account Holder Name: John Doe
>>    -
>>
>>    Account Number: 1234567890
>>    -
>>
>>    Date of Transaction: March 18, 2025
>>    -
>>
>>    Amount Debited: $5,000 USD
>>
>> I kindly request your immediate assistance in investigating this matter
>> and taking necessary actions to secure my account. Additionally, I would
>> appreciate it if you could provide any supporting evidence or verification
>> that may assist in identifying the unauthorized activity. Enclosed with
>> this email is a verification letter dated March 19, 2025, issued by your
>> bank, confirming my account details and available balance.
>>
>> Please treat this matter as urgent. For any further clarification, feel
>> free to contact me at +1 (123) 456-7890 or johndoe@example.com.
>>
>> Thank you for your prompt support.
>>
>> Sincerely,
>>
>> John Doe
>>
>> 123 Maple Street Cityville,
>>
>> Countryland
>>
>> +1 (123) 456-7890
>>
>> johndoe@example.com
>>
>
  """
# print("Original:", input_text)
# print("Cleaned:", clean_text(input_text))