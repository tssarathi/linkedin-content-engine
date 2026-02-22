import json

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from content_agent.pipeline import root_agent
from shared.prompt_parser import parse_prompt
from research_agent.graph import app


async def run_pipeline(user_input: str) -> str:
    request, github_url = parse_prompt(user_input)

    state = await app.ainvoke({"request": request, "GA_repo_url": github_url})

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
