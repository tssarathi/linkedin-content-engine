from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from content_agent.prompts.editor_instruction import DESCRIPTION, INSTRUCTION
from content_agent.schemas.editor_schema import EditorReview


def _escalate_on_approval(callback_context: CallbackContext) -> None:
    """Break out of the LoopAgent early when the editor approves the draft."""
    review = callback_context.state.get("editor_review")
    if review and review.get("approved"):
        callback_context._event_actions.escalate = True
        callback_context.state["editor_approved"] = True


editor_agent = Agent(
    name="editor",
    model="gemini-2.0-flash",
    description=DESCRIPTION,
    instruction=INSTRUCTION,
    output_key="editor_review",
    output_schema=EditorReview,
    after_agent_callback=_escalate_on_approval,
)
