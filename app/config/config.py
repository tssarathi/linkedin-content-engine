import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # -- Tool API Keys --
    RA_GA_GITHUB_API_KEY = os.getenv("RA_GA_GITHUB_API_KEY")
    RA_NR_SERPER_API_KEY = os.getenv("RA_NR_SERPER_API_KEY")
    RA_TA_EXA_API_KEY = os.getenv("RA_TA_EXA_API_KEY")
    RA_FC_TAVILY_API_KEY = os.getenv("RA_FC_TAVILY_API_KEY")


config = Config()
