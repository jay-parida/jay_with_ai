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

from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    phone: str
    problem: str

schema =Ticket.model_json_schema()
response_format={
"type":"json_object"
}
system_prompt=f"""
You are a JSON extraction assistant. Extract the personal information from the ticket and respond with ONLY valid JSON, no additional text or explanation you can mention in line by line.
Schema: {schema}
"""
system_message = {
    "role": "system",
    "content": system_prompt
    }
text="Hi my name is jayaram parida and i have purchased one Iphone 15 pro max and i have a problem with the camera and my address is bangalore and my phone number is 1234567890 and my email is jayaram.parida@example.com"
prompt=f"""
Extract information from this ticket: {text}

Return ONLY the JSON object, no additional text."""

message = {"role": role, "content": prompt}
messages = [system_message, message]
response=client.chat.completions.create(
    model=model,messages=messages)
answer=response.choices[0].message.content
#print(answer)

import json
raw_json =answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)
print(ticket.name)
print(ticket.email)
print(ticket.phone)