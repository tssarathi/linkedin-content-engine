from google.adk.agents.llm_agent import Agent

from content_agent.instruction.editor_instruction import DESCRIPTION, INSTRUCTION
from content_agent.schemas.editor_schema import EditorReview

editor_agent = Agent(
    name="editor",
    model="gemini-2.5-flash-lite",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="editor_review",
    output_schema=EditorReview,
)
