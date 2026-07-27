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
role="user"
prompt1="Hi"
prompt2="Write a short story about a robot learning to love.under 100 words"
prompt3="Write a short story about a virat kohli"
prompts = [prompt1, prompt2, prompt3]   
for prompt in prompts:
    message = {"role": role, "content": prompt}
    messages = [message]
    response=client.chat.completions.create(
    model=model,messages=messages,max_tokens=100)
    usage =response.usage
    print(f"Prompt: {prompt}")
    print(f"Usage: {usage}")
    print(f"finish reason: {response.choices[0].finish_reason}")