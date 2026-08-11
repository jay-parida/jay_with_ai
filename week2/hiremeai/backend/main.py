import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader

# ------------------ SETUP ------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not set")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-120b"

app = FastAPI()

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

# ------------------ MODELS ------------------
class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

resume_schema = Resume.model_json_schema()

class ChatRequest(BaseModel):
    question: str

# ------------------ PDF ------------------
def read_pdf(file_path: Path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ------------------ PARSE RESUME ------------------
def parse_resume(resume_text):
    system_prompt = f"""
You are an expert resume parser.

Return ONLY valid JSON matching this schema:
{resume_schema}

Rules:
- Do not invent info
- Missing → null
- Empty list if none
"""

    user_prompt = f"Parse this resume:\n{resume_text}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return Resume(**data)

# ------------------ AI CHAT ------------------
def ask_candidate(question: str, resume: Resume):
    system_prompt = f"""
You are a job candidate.

Candidate data:
{resume.model_dump_json(indent=2)}

Rules:
- Answer like a human
- Be confident but honest
- No hallucination
- If unknown → "I don't have enough information"
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content

# ------------------ CACHE ------------------
cached_resume = None

@app.on_event("startup")
def load_resume():
    global cached_resume
    resume_text = read_pdf(Path("alex_rivera_resume.pdf"))
    cached_resume = parse_resume(resume_text)

# ------------------ ROUTES ------------------
@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_candidate(request.question, cached_resume)
    return {"answer": answer}