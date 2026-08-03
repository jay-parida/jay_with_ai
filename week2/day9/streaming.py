import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"
prompt="Explain how a neural network works in 1000 words. Use simple language and examples. Make it easy to understand for a 10-year-old."
message={"role":"user","content":prompt}
messages=[message]
# response=client.chat.completions.create(model=model,messages=messages)
# answer=response.choices[0].message.content
# print(answer)

stream_response=client.chat.completions.create(model=model,messages=messages,stream=True)
for chunk in stream_response:
    content=chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)