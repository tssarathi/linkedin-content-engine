import asyncio
import pprint as pp

from research_agent.agents.synthesizer_agent import synthesizer_agent
from research_agent.state import ResearchState


async def main() -> None:
    state: ResearchState = {
        "request": "Write a LinkedIn post about my multi-agent content engine project",
        "post_type": "project_showcase",
        "GA_project_analysis": {
            "summary": (
                "A multi-agent LinkedIn content engine that orchestrates research "
                "agents via LangGraph. It uses MCP for tool integration (GitHub, "
                "Exa, Tavily) and produces structured research briefs that feed "
                "into a content generation service."
            ),
            "tech_stack": ["Python", "LangGraph", "FastAPI", "Pydantic", "Groq"],
            "recent_activity": "Added Fact Checker agent with Tavily MCP verification loop",
            "key_features": [
                "Multi-agent orchestration with LangGraph StateGraph",
                "MCP stdio transport for GitHub, Exa, and Tavily tools",
                "Hybrid search: DuckDuckGo (keyword) + Exa (semantic)",
                "Fact-checking with loop-back for unverified claims",
                "Structured output via Pydantic schemas at every stage",
            ],
        },
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
                        "enabling cross-framework agent communication. "
                        "Early adopters report 60% faster integration times."
                    ),
                    "relevance": "Related to multi-agent architecture patterns.",
                },
                {
                    "title": "Groq Inference Speed Doubles with New Hardware",
                    "url": "https://groq.com/blog/lpu-v2",
                    "summary": (
                        "Groq's latest LPU chip delivers 2x throughput, "
                        "making real-time multi-agent pipelines feasible "
                        "at production scale."
                    ),
                    "relevance": "Project uses Groq for all agent LLM inference.",
                },
            ],
            "search_queries_used": [
                "LangGraph latest release 2026",
                "AI agent frameworks news February 2026",
                "MCP protocol tools integration 2026",
            ],
            "topic_summary": (
                "Multi-agent AI systems are rapidly evolving with new "
                "orchestration frameworks, tool protocols like MCP, and "
                "faster inference hardware from Groq."
            ),
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
                {
                    "topic": "Build-in-Public AI Projects",
                    "description": (
                        "Engineers sharing their AI agent builds on LinkedIn "
                        "are seeing 3-5x engagement compared to tutorial content. "
                        "Authenticity and real failure stories drive engagement."
                    ),
                    "source_url": "https://linkedin.com/pulse/build-public-ai",
                },
                {
                    "topic": "Agent Orchestration Frameworks",
                    "description": (
                        "LangGraph, CrewAI, and AutoGen are competing for the "
                        "multi-agent framework space. LangGraph's graph-based "
                        "approach is gaining traction among production teams."
                    ),
                    "source_url": "https://blog.langchain.dev/agent-frameworks-2026",
                },
            ],
            "recommended_hashtags": [
                "#AI",
                "#AIAgents",
                "#LangGraph",
                "#MCP",
                "#BuildInPublic",
                "#MultiAgent",
                "#Python",
            ],
            "content_patterns": [
                "Build-in-public threads with architecture diagrams",
                "Before/after comparisons showing agent improvements",
                "Hot takes on framework choices with real benchmarks",
                "Step-by-step breakdowns of agent pipelines",
            ],
            "engagement_insights": (
                "Technical deep-dives with real code snippets and architecture "
                "diagrams are outperforming generic AI hot takes. Posts that "
                "show a specific problem → solution → result arc get the "
                "highest engagement, especially when they include honest "
                "reflections on what didn't work."
            ),
            "search_queries_used": [
                "multi-agent orchestration trends LinkedIn 2026",
                "AI engineering content engagement patterns",
                "LangGraph MCP trending posts",
            ],
        },
        "FC_fact_check_results": {
            "claim_verifications": [
                {
                    "claim": "LangGraph 0.3 released with built-in MCP tool integration",
                    "status": "verified",
                    "confidence": 0.9,
                    "source_url": "https://blog.langchain.dev/langgraph-0-3",
                    "reasoning": (
                        "Confirmed via the official LangChain blog. LangGraph 0.3 "
                        "was released in January 2026 with native MCP support."
                    ),
                },
                {
                    "claim": "MCP boilerplate reduction of 40%",
                    "status": "partially_verified",
                    "confidence": 0.5,
                    "source_url": "https://blog.langchain.dev/langgraph-0-3",
                    "reasoning": (
                        "The blog mentions 'significant reduction in boilerplate' "
                        "but does not cite a specific 40% figure."
                    ),
                },
                {
                    "claim": "Google open-sourced the A2A protocol",
                    "status": "verified",
                    "confidence": 0.95,
                    "source_url": "https://github.com/google/a2a-protocol",
                    "reasoning": (
                        "Confirmed via the official Google Developers Blog "
                        "and the public GitHub repository."
                    ),
                },
                {
                    "claim": "Over 500 MCP servers available in the ecosystem",
                    "status": "unverified",
                    "confidence": 0.4,
                    "source_url": None,
                    "reasoning": (
                        "Could not find an authoritative source for this "
                        "specific count. The MCP ecosystem is growing but "
                        "the exact number is not independently confirmed."
                    ),
                },
            ],
            "search_queries_used": [
                "LangGraph 0.3 release date MCP support",
                "Google A2A protocol open source 2026",
                "MCP servers ecosystem count 2026",
            ],
            "summary": (
                "3 out of 4 claims checked. 2 verified, 1 partially verified, "
                "1 unverified. Core technical claims about LangGraph and A2A are "
                "solid. The MCP ecosystem size claim should be hedged."
            ),
        },
    }

    brief = await synthesizer_agent(state)
    pp.pprint(brief)


if __name__ == "__main__":
    asyncio.run(main())
