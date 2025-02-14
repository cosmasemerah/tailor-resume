from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    SerperDevTool
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResumeTools:
    """Tools for the resume tailor agents"""
    
    def __init__(self, resume_path='./fake_resume.md'):
        """Initialize tools with configurable resume path"""
        self.search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
        self.scrape_tool = ScrapeWebsiteTool()
        self.read_resume = FileReadTool(file_path=resume_path)

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