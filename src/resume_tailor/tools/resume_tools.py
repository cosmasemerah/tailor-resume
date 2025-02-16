from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    SerperDevTool
)
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResumeTools:
    """Tools for the resume tailor agents"""
    
    def __init__(self, resume_content: str):
        """Initialize tools with resume content"""
        self.search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
        self.scrape_tool = ScrapeWebsiteTool()
        
        # Create a temporary file with the content
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md')
        self.temp_file.write(resume_content)
        self.temp_file.close()
        self.read_resume = FileReadTool(file_path=self.temp_file.name)

    def __del__(self):
        """Cleanup temporary file if it exists"""
        if hasattr(self, 'temp_file') and os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except:
                pass

    def get_researcher_tools(self):
        """Get tools for the researcher agent"""
        return [self.scrape_tool, self.search_tool]

    def get_profile_tools(self):
        """Get tools for the profiler agent"""
        return [
            self.scrape_tool,
            self.search_tool,
            self.read_resume
        ]

    def get_resume_tools(self):
        """Get tools for the resume strategist agent"""
        return [
            self.scrape_tool,
            self.search_tool,
            self.read_resume
        ]

    def get_interview_tools(self):
        """Get tools for the interview preparer agent"""
        return [
            self.scrape_tool,
            self.search_tool,
            self.read_resume
        ] 