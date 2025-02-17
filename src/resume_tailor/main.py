#!/usr/bin/env python
import sys
import warnings
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from resume_tailor.crew import ResumeTailor

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(
    title="Resume Tailor API",
    description="API for tailoring resumes based on job postings using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TailorRequest(BaseModel):
    job_posting_url: str
    github_url: str
    personal_writeup: str
    resume_content: str

@app.post("/api/tailor")
async def tailor_resume(request: TailorRequest):
    """
    Tailor a resume based on the job posting and personal information.
    """
    try:
        crew = ResumeTailor(resume_content=request.resume_content)
        
        inputs = {
            'job_posting_url': request.job_posting_url,
            'github_url': request.github_url,
            'personal_writeup': request.personal_writeup
        }
        
        result = crew.crew().kickoff(inputs=inputs)

        # The research_task output will now be a JobResearch model
        research_output = result.research_task.pydantic

        return {
            "status": "success",
            "message": "Resume tailored successfully",
            "data": {
                "title": f"{research_output.job_title} at {research_output.company}",
                "resume_strategy_task": result.resume_strategy_task.raw,
                "interview_preparation_task": result.interview_preparation_task.raw
            }
        }
    except Exception as e:
        error_message = str(e)
        status_code = 500
        error_type = "Internal Server Error"
        
        # Check if it's a rate limit error
        if "rate limit" in error_message.lower():
            status_code = 429
            error_type = "Rate Limit Exceeded"
            error_message = "The AI service is currently at capacity. Please wait a few minutes and try again."
        
        raise HTTPException(
            status_code=status_code,
            detail={
                "type": error_type,
                "message": error_message
            }
        )

def run():
    """Run the FastAPI server using uvicorn."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'job_posting_url': 'https://job-boards.greenhouse.io/perplexityai/jobs/4148325007',
        'github_url': 'https://github.com/cosmasemerah',
        'personal_writeup': """Cosmas is a skilled Full Stack Developer with expertise in 
        JavaScript/TypeScript, Python, and modern web frameworks. He has successfully delivered 
        multiple high-impact projects and has experience in AI/ML integration."""
    }
    try:
        ResumeTailor().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResumeTailor().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'job_posting_url': 'https://job-boards.greenhouse.io/perplexityai/jobs/4148325007',
        'github_url': 'https://github.com/cosmasemerah',
        'personal_writeup': """Cosmas is a skilled Full Stack Developer with expertise in 
        JavaScript/TypeScript, Python, and modern web frameworks. He has successfully delivered 
        multiple high-impact projects and has experience in AI/ML integration."""
    }
    try:
        ResumeTailor().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
