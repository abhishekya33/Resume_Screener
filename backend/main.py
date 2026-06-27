from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uuid
import os
import tempfile

from services.ranking_service import ResumeRanker
from utils.pdf_parser import extract_text_from_pdf, extract_text_from_docx, clean_text

# Create FastAPI app
app = FastAPI(title="AI Resume Screener API", description="Smart resume screening system", version="1.0.0")

# Enable CORS for frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-app.vercel.app", 
        "http://localhost:5173"                 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ranker
print("Starting Resume Screener API...")
ranker = ResumeRanker()

# In-memory storage
resumes_db = {}
job_descriptions = {}

# Request/Response Models
class RankRequest(BaseModel):
    job_description_id: str
    resume_ids: List[str]

class JobDescriptionRequest(BaseModel):
    text: str

class RankResponse(BaseModel):
    rankings: List[dict]
    
# API Endpoints

@app.get("/")
async def root():
    return {"message": "AI Resume Screener API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "resumes_loaded": len(resumes_db)}

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume"""
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1].lower()
    
    # Validate file type
    if file_extension not in ['pdf', 'docx']:
        raise HTTPException(400, "Only PDF and DOCX files are supported")
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Extract text based on file type
        if file_extension == 'pdf':
            text = extract_text_from_pdf(temp_path)
        else:  # docx
            text = extract_text_from_docx(temp_path)
        
        if not text or len(text.strip()) < 50:
            os.unlink(temp_path)
            raise HTTPException(400, "Could not extract enough text from file. Please ensure it's not scanned/image-based.")
        
        # Clean text
        text = clean_text(text)
        
        # Store
        resumes_db[file_id] = {
            'id': file_id,
            'filename': file.filename,
            'text': text
        }
        
        return JSONResponse(content={
            'resume_id': file_id, 
            'filename': file.filename,
            'text_length': len(text)
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.post("/api/job-description")
async def create_job_description(request: JobDescriptionRequest):
    """Store a job description"""
    jd_text = request.text
    if not jd_text or len(jd_text.strip()) < 10:
        raise HTTPException(400, "Job description is too short (minimum 10 characters)")
    
    jd_id = str(uuid.uuid4())
    job_descriptions[jd_id] = jd_text
    return {'job_description_id': jd_id}

@app.post("/api/rank")
async def rank_resumes(request: RankRequest):
    """Rank resumes against a job description"""
    if request.job_description_id not in job_descriptions:
        raise HTTPException(404, "Job description not found")
    
    resumes = []
    for resume_id in request.resume_ids:
        if resume_id not in resumes_db:
            raise HTTPException(404, f"Resume {resume_id} not found")
        resumes.append(resumes_db[resume_id])
    
    if len(resumes) == 0:
        raise HTTPException(400, "No resumes to rank")
    
    jd_text = job_descriptions[request.job_description_id]
    rankings = ranker.rank_multiple_resumes(jd_text, resumes)
    
    return RankResponse(rankings=rankings)

@app.get("/api/resumes")
async def get_all_resumes():
    """Get all uploaded resumes"""
    return list(resumes_db.values())

@app.delete("/api/resumes/{resume_id}")
async def delete_resume(resume_id: str):
    """Delete a resume"""
    if resume_id in resumes_db:
        del resumes_db[resume_id]
        return {"message": "Resume deleted"}
    raise HTTPException(404, "Resume not found")

@app.delete("/api/job-descriptions/{jd_id}")
async def delete_job_description(jd_id: str):
    """Delete a job description"""
    if jd_id in job_descriptions:
        del job_descriptions[jd_id]
        return {"message": "Job description deleted"}
    raise HTTPException(404, "Job description not found")