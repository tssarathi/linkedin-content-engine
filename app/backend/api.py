from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.linkedin_content_engine import get_post
from app.utilities.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="LinkedIn Content Engine",
    description="A LinkedIn content engine that generates content for LinkedIn posts",
)


class RequestState(BaseModel):
    prompt: str


@app.post("/request")
async def request_endpoint(request: RequestState):
    logger.info(f"Request received: {request}")

    try:
        post = await get_post(request.prompt)
        logger.info(f"Post generated: {post}")

        return {"post": post}

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
