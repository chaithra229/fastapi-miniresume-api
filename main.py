
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
import os
import shutil
from typing import Optional

app = FastAPI()

candidates = []
candidate_id = 1

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/candidates")
def create_candidate(
    full_name: str = Form(...),
    dob: str = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education: str = Form(...),
    graduation_year: int = Form(...),
    experience: int = Form(...),
    skills: str = Form(...),
    resume: UploadFile = File(...)
):
    global candidate_id

    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    candidate = {
        "id": candidate_id,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education": education,
        "graduation_year": graduation_year,
        "experience": experience,
        "skills": skills,
        "resume_filename": resume.filename
    }

    candidates.append(candidate)
    candidate_id += 1

    return {"message": "Candidate created", "candidate": candidate}


@app.get("/candidates")
def list_candidates(
    skill: Optional[str] = Query(None),
    experience: Optional[int] = Query(None),
    graduation_year: Optional[int] = Query(None)
):
    result = candidates

    if skill:
        result = [c for c in result if skill.lower() in c["skills"].lower()]

    if experience is not None:
        result = [c for c in result if c["experience"] == experience]

    if graduation_year is not None:
        result = [c for c in result if c["graduation_year"] == graduation_year]

    return result


@app.get("/candidates/{id}")
def get_candidate(id: int):
    for candidate in candidates:
        if candidate["id"] == id:
            return candidate
    raise HTTPException(status_code=404, detail="Candidate not found")


@app.delete("/candidates/{id}")
def delete_candidate(id: int):
    for candidate in candidates:
        if candidate["id"] == id:
            candidates.remove(candidate)
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Candidate not found")