import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # -- GitHub Analyser --
    RA_GA_GROQ_API_KEY = os.getenv("RA_GA_GROQ_API_KEY")
    RA_GA_GITHUB_API_KEY = os.getenv("RA_GA_GITHUB_API_KEY")

    # -- News Researcher --
    RA_NR_GROQ_API_KEY = os.getenv("RA_NR_GROQ_API_KEY")
    RA_NR_SERPER_API_KEY = os.getenv("RA_NR_SERPER_API_KEY")

    # -- Trend Analyser --
    RA_TA_GROQ_API_KEY = os.getenv("RA_TA_GROQ_API_KEY")
    RA_TA_EXA_API_KEY = os.getenv("RA_TA_EXA_API_KEY")

    # -- Fact Checker --
    RA_FC_GROQ_API_KEY = os.getenv("RA_FC_GROQ_API_KEY")
    RA_FC_TAVILY_API_KEY = os.getenv("RA_FC_TAVILY_API_KEY")

    # -- Synthesizer --
    RA_SY_GROQ_API_KEY = os.getenv("RA_SY_GROQ_API_KEY")

    # -- Supervisor --
    RA_SU_GROQ_API_KEY = os.getenv("RA_SU_GROQ_API_KEY")


config = Config()
