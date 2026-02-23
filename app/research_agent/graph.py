from langgraph.graph import END, START, StateGraph

from research_agent.agents.fact_checker_agent import fact_checker_agent
from research_agent.agents.github_analyser_agent import github_analyser_agent
from research_agent.agents.news_researcher_agent import news_researcher_agent
from research_agent.agents.supervisor import supervisor_agent
from research_agent.agents.synthesizer_agent import synthesizer_agent
from research_agent.agents.trend_analyser_agent import trend_analyser_agent
from research_agent.state import ResearchState


def after_start(state: ResearchState) -> str:
    if state.get("GA_repo_url"):
        return "github_analyser"
    return "supervisor"


graph = StateGraph(ResearchState)

# -- Nodes --
graph.add_node("github_analyser", github_analyser_agent)
graph.add_node("news_researcher", news_researcher_agent)
graph.add_node("trend_analyser", trend_analyser_agent)
graph.add_node("fact_checker", fact_checker_agent)
graph.add_node("synthesizer", synthesizer_agent)
graph.add_node("supervisor", supervisor_agent)

# -- Edges --
graph.add_conditional_edges(START, after_start)

graph.add_edge("github_analyser", "supervisor")

graph.add_edge("supervisor", "news_researcher")
graph.add_edge("supervisor", "trend_analyser")
graph.add_edge(["news_researcher", "trend_analyser"], "fact_checker")

graph.add_edge("fact_checker", "synthesizer")
graph.add_edge("synthesizer", END)

app = graph.compile()
