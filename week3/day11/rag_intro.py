import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

#step 1: Create a knowledge base
knowledge_base={
    "age": "Jayaram is 30 years old.",
    "profession": "Jayaram is a teacher.",
    "net worth": "Jayaram has a net worth of $500,000.",
}

#step-2: retrieve relevant information from the knowledge base
def retrieve_info(question):
    question_lower = question.lower()
    if "age" in question_lower:
        return knowledge_base["age"]
    elif "profession" in question_lower:
        return knowledge_base["profession"]
    elif "net worth" in question_lower:
        return knowledge_base["net worth"]
    else:
        return "I don't have information about that."
    
def ask_llm(question):
    context = retrieve_info(question)
    sys_prompt = "Answer in one line only, based on the following context: " + context + "do not hallucinate or make up information."
    system_message = {
        "role": "system",
        "content": sys_prompt
    }
    message = {
        "role": "user",
        "content": question
    }
    messages = [system_message, message]
    response =client.chat.completions.create(
        model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

question = "Do you know Jayaram?"
print(ask_llm(question))