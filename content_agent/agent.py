from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent

from content_agent.agents.copywriter_agent import copywriter_agent
from content_agent.agents.editor_agent import editor_agent
from content_agent.agents.optimizer_agent import optimizer_agent
from content_agent.agents.strategist_agent import strategist_agent

writing_team = LoopAgent(
    name="writing_team",
    description="Iteratively drafts and reviews a LinkedIn post — the Copywriter writes, the Editor scores and approves or requests one revision, cycling up to 2 times.",
    sub_agents=[copywriter_agent, editor_agent],
    max_iterations=2,
)

pipeline = SequentialAgent(
    name="content_pipeline",
    description="End-to-end LinkedIn content pipeline: Strategist sets the angle, writing_team drafts and edits, Optimizer produces the final publish-ready post.",
    sub_agents=[strategist_agent, writing_team, optimizer_agent],
)

root_agent = pipeline
