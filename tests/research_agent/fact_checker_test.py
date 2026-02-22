import asyncio

from research_agent.agents.fact_checker_agent import fact_checker_agent
from research_agent.state import ResearchState


async def test_fact_checker() -> None:
    state: ResearchState = {
        "request": "AI agents and multi-agent systems using LangGraph",
        "NR_news_findings": {
            "news_items": [
                {
                    "title": "LangGraph 0.3 Released with Native MCP Support",
                    "url": "https://blog.langchain.dev/langgraph-mcp",
                    "summary": (
                        "LangChain announced LangGraph 0.3 with built-in MCP "
                        "tool integration, reducing boilerplate for multi-agent "
                        "systems by 40%."
                    ),
                    "relevance": "Directly relevant to the project's tech stack.",
                },
                {
                    "title": "Google Releases A2A Protocol for Agent Communication",
                    "url": "https://developers.googleblog.com/a2a-protocol",
                    "summary": (
                        "Google open-sourced the Agent-to-Agent protocol, "
                        "enabling cross-framework agent communication."
                    ),
                    "relevance": "Related to multi-agent architecture patterns.",
                },
            ],
            "search_queries_used": [
                "LangGraph latest release 2026",
                "AI agent frameworks news February 2026",
            ],
            "topic_summary": "Multi-agent AI systems are rapidly evolving.",
        },
        "TA_trend_data": {
            "trending_topics": [
                {
                    "topic": "MCP Protocol Adoption",
                    "description": (
                        "The Model Context Protocol is seeing rapid adoption "
                        "across AI tooling, with over 500 MCP servers now "
                        "available in the ecosystem."
                    ),
                    "source_url": "https://modelcontextprotocol.io/blog/adoption",
                },
            ],
            "recommended_hashtags": ["#AI", "#LangGraph", "#MCP", "#AIAgents"],
            "content_patterns": ["Build-in-public threads", "Tool comparison posts"],
            "engagement_insights": "Technical deep-dives are outperforming hot takes.",
            "search_queries_used": ["multi-agent orchestration trends LinkedIn 2026"],
        },
    }

    results = await fact_checker_agent(state)

    fc = results.get("FC_fact_check_results")
    assert fc is not None, "FC_fact_check_results should not be None"
    assert len(fc["claim_verifications"]) >= 1, "should have at least 1 claim verification"
    assert fc["summary"], "summary should not be empty"
    print("PASS: Fact Checker")


async def main() -> None:
    await test_fact_checker()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
