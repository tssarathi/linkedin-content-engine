from google.adk.agents import Agent

from app.content_agent.prompts.copywriter_instruction import DESCRIPTION, INSTRUCTION

copywriter_agent = Agent(
    name="copywriter",
    model="gemini-2.5-flash-lite",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="post_draft",
)
