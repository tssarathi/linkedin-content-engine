import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # -- GitHub Analyser --
    RA_GA_GROQ_API_KEY = os.getenv("RA_GA_GROQ_API_KEY")
    RA_GA_GITHUB_API_KEY = os.getenv("RA_GA_GITHUB_API_KEY")


config = Config()
