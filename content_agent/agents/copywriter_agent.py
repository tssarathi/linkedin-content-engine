from google.adk.agents import Agent

from content_agent.prompts.copywriter_instruction import DESCRIPTION, INSTRUCTION

copywriter_agent = Agent(
    name="copywriter",
    model="gemini-2.0-flash",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="post_draft",
)
