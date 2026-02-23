import asyncio
import json
import sys

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
from openinference.instrumentation.google_adk import GoogleADKInstrumentor

from app.content_service.agent import root_agent
from app.utilities.prompt_parser import parse_prompt
from app.research_service.graph import graph as research_graph

GoogleADKInstrumentor().instrument()


async def run_pipeline(user_input: str) -> str:
    request, github_url = parse_prompt(user_input)

    langfuse_handler = LangfuseCallbackHandler()
    state = await research_graph.ainvoke(
        {"request": request, "GA_repo_url": github_url},
        config={"callbacks": [langfuse_handler]},
    )

    research_brief = state["research_brief"]
    research_brief_json = json.dumps(research_brief)

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="linkedin_content_engine",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="linkedin_content_engine", user_id="user"
    )

    async for event in runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=types.Content(
            role="user", parts=[types.Part(text=research_brief_json)]
        ),
    ):
        pass

    session_state = await session_service.get_session(
        app_name="linkedin_content_engine", user_id="user", session_id=session.id
    )
    linkedin_post = session_state.state.get("linkedin_post")
    return linkedin_post["publish_ready_post"]


async def main():
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your prompt: ")
    post = await run_pipeline(user_input)
    print(post)


if __name__ == "__main__":
    asyncio.run(main())
