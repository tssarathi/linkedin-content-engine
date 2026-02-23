from google.adk.agents import Agent

from app.core.content_service.prompts.copywriter_prompt import DESCRIPTION, INSTRUCTION

copywriter_agent = Agent(
    name="copywriter",
    model="gemini-3-flash-preview",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="post_draft",
)
