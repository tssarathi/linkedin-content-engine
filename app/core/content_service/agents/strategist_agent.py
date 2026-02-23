from google.adk.agents import Agent

from app.core.content_service.prompts.strategist_prompt import DESCRIPTION, INSTRUCTION
from app.core.content_service.schemas.strategy_schema import StrategyDocument

strategist_agent = Agent(
    name="strategist",
    model="gemini-3-flash-preview",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="strategy_document",
    output_schema=StrategyDocument,
)
