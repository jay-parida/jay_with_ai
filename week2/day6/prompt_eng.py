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

def llm_ans(prompt):
    message = {"role": "user", "content": prompt}
    messages = [message]
    response=client.chat.completions.create(
        model=model,messages=messages)
    ans=response.choices[0].message.content
    return ans

# prompt to classify the complaint
bad_prompt="""
#Role
You are support assistant at a mobile/laptop company
#Task
You have to classify the issue in category
#Constraints
You have to classify the issue in one of the three categories:billing, technical, return
#Ouput Format
You have to output the category in one word only
#zero-shot example
For instance if a user complaint is "I have been charged twice for my last purchase", you should output "billing"
#FallBack
If you are not able to classify the issue, you should output "Other issue"
This is a user complaint
My laptop is not working
"""
print(llm_ans(bad_prompt))