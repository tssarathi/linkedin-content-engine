from google.adk.agents.llm_agent import Agent

from content_agent.prompts.strategist_instruction import DESCRIPTION, INSTRUCTION
from content_agent.schemas.strategy_schema import StrategyDocument

strategist_agent = Agent(
    name="strategist",
    model="gemini-2.5-flash-lite",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="strategy_document",
    output_schema=StrategyDocument,
)
