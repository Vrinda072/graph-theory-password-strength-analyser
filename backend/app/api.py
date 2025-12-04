# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .password_analyzer import PasswordAnalyzer

app = FastAPI(title="Graph Theory Password Strength Analyzer")
_analyzer = PasswordAnalyzer()

class PWRequest(BaseModel):
    password: str

@app.post('/analyze')
def analyze_pw(req: PWRequest):
    pw = req.password
    if not pw:
        raise HTTPException(status_code=400, detail="Password required")
    trace = _analyzer.analyze(pw)
    return trace

@app.get('/health')
def health():
    return {"status": "ok"}
