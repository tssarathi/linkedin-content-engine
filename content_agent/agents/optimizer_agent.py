from google.adk.agents.llm_agent import Agent

from content_agent.prompts.optimizer_instruction import DESCRIPTION, INSTRUCTION
from content_agent.schemas.linkedin_post_schema import LinkedInPost

optimizer_agent = Agent(
    name="optimizer",
    model="gemini-2.5-flash",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="linkedin_post",
    output_schema=LinkedInPost,
)
