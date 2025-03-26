from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"  # The model you want to use

# Initialize ChatGroq
llm = ChatGroq(api_key=API_KEY, model_name=MODEL_NAME)

def classify_query(query):
    response = llm.invoke(f"""
    You are a banking AI assistant. Classify the user's query into:
    - Request Type
    - Sub Request Type
    - Reason
    - Confidence Level (0-100%)
    - Priority (Low, Medium, High)

    User Query: {query}
    """)
    
    return response.content

# Example usage
if __name__ == "__main__":
    query = " I am facing issues with my online banking account. I can't log in and I need help to reset my password"
    result = classify_query(query)
    print("LLM Response:", result)