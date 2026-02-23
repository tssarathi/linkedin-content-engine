from google.adk.agents import Agent

from app.core.content_service.prompts.optimizer_prompt import DESCRIPTION, INSTRUCTION
from app.core.content_service.schemas.linkedin_post_schema import LinkedInPost

optimizer_agent = Agent(
    name="optimizer",
    model="gemini-2.5-flash-lite",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="linkedin_post",
    output_schema=LinkedInPost,
)
