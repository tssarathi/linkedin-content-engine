from langgraph.graph import END, START, StateGraph

from app.research_service.agents.fact_checker_agent import fact_checker_agent
from app.research_service.agents.github_analyser_agent import github_analyser_agent
from app.research_service.agents.news_researcher_agent import news_researcher_agent
from app.research_service.agents.supervisor_agent import supervisor_agent
from app.research_service.agents.synthesizer_agent import synthesizer_agent
from app.research_service.agents.trend_analyser_agent import trend_analyser_agent
from app.research_service.state import ResearchState


def after_start(state: ResearchState) -> str:
    if state.get("GA_repo_url"):
        return "github_analyser"
    return "supervisor"


builder = StateGraph(ResearchState)

# -- Nodes --
builder.add_node("github_analyser", github_analyser_agent)
builder.add_node("news_researcher", news_researcher_agent)
builder.add_node("trend_analyser", trend_analyser_agent)
builder.add_node("fact_checker", fact_checker_agent)
builder.add_node("synthesizer", synthesizer_agent)
builder.add_node("supervisor", supervisor_agent)

# -- Edges --
builder.add_conditional_edges(START, after_start)

builder.add_edge("github_analyser", "supervisor")

builder.add_edge("supervisor", "news_researcher")
builder.add_edge("supervisor", "trend_analyser")
builder.add_edge(["news_researcher", "trend_analyser"], "fact_checker")

builder.add_edge("fact_checker", "synthesizer")
builder.add_edge("synthesizer", END)

graph = builder.compile()
