import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # -- Tool API Keys --
    RS_GA_GITHUB_API_KEY = os.getenv("RS_GA_GITHUB_API_KEY")
    RS_NR_SERPER_API_KEY = os.getenv("RS_NR_SERPER_API_KEY")
    RS_TA_EXA_API_KEY = os.getenv("RS_TA_EXA_API_KEY")
    RS_FC_TAVILY_API_KEY = os.getenv("RS_FC_TAVILY_API_KEY")


config = Config()
