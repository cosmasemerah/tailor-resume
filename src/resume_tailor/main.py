#!/usr/bin/env python
import sys
import warnings
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        # Read the output files that were generated
        try:
            with open('tailored_resume.md', 'r') as f:
                resume_content = f.read()
            with open('interview_materials.md', 'r') as f:
                interview_content = f.read()
        except FileNotFoundError as e:
            logger.error(f"Could not read output files: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "type": "File Not Found",
                    "message": f"Could not read output files: {str(e)}"
                }
            )
        
        # Get the job title and company from the first task's output
        try:
            research_output = result.outputs[0]  # First task's output
            logger.info(f"Research task output type: {type(research_output)}")
            logger.info(f"Research task output: {research_output}")
            
            if isinstance(research_output, dict):
                job_title = research_output.get('job_title', 'Position')
                company = research_output.get('company', 'Company')
                title = f"{job_title} at {company}"
                logger.info(f"Successfully extracted job details: {title}")
            else:
                title = "Job Application"
                logger.warning(f"Research task output was not in expected format. Got: {type(research_output)}")
        except (AttributeError, IndexError) as e:
            title = "Job Application"
            logger.error(f"Could not extract job details from research task: {str(e)}")

        return {
            "status": "success",
            "message": "Resume tailored successfully",
            "data": {
                "title": title,
                "resume_strategy_task": resume_content,
                "interview_preparation_task": interview_content
            }
        }
    
    except Exception as e:
        error_message = str(e)
        status_code = 500
        error_type = "Internal Server Error"
        
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
