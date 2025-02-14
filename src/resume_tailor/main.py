#!/usr/bin/env python
import sys
import warnings

from resume_tailor.crew import ResumeTailor

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'job_posting_url': 'https://job-boards.greenhouse.io/perplexityai/jobs/4148325007',
        'github_url': 'https://github.com/cosmasemerah',
        'personal_writeup': """Cosmas is a skilled Full Stack Developer with a proven track record 
        in building scalable web applications. With expertise in JavaScript/TypeScript, Python, 
        and modern frameworks like Next.js and React, he has successfully delivered multiple 
        high-impact projects. Notable achievements include developing a SaaS platform that 
        generated ₦2M+ in revenue within 8 weeks and implementing significant performance 
        optimizations resulting in 40% LCP improvement. Cosmas has strong experience in 
        database management (Supabase, MongoDB), security implementations, and UI/UX design. 
        His background in Mathematics & Statistics, combined with certifications in AI and 
        deep learning, demonstrates his analytical approach and commitment to staying current 
        with emerging technologies. He excels in technical leadership, cross-functional 
        collaboration, and has a proven ability to mentor junior developers."""
    }
    
    try:
        ResumeTailor().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


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
