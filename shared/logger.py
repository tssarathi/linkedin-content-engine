import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import langchain_mcp_adapters.sessions as _lma_sessions
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client as _stdio_client

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)

logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.DEBUG,
)


class _ShortNameFormatter(logging.Formatter):
    def format(self, record):
        record.short_name = record.name.split(".")[-1]
        return super().format(record)


_root = logging.getLogger()
_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(_ShortNameFormatter("[%(short_name)s] %(message)s"))
_root.addHandler(_console)

# Suppress third-party loggers
for _name in (
    "langchain",
    "langchain_core",
    "langchain_community",
    "httpx",
    "httpcore",
):
    logging.getLogger(_name).setLevel(logging.WARNING)

# Redirect MCP subprocess stderr to devnull (suppresses smithery/exa/tavily noise)
_devnull = open(os.devnull, "w")


_DEFAULT_ENCODING = "utf-8"
_DEFAULT_ENCODING_ERROR_HANDLER = "strict"


@asynccontextmanager
async def _quiet_create_stdio_session(
    *,
    command: str,
    args: list[str],
    env: dict[str, str] | None = None,
    cwd: str | Path | None = None,
    encoding: str = _DEFAULT_ENCODING,
    encoding_error_handler: Literal[
        "strict", "ignore", "replace"
    ] = _DEFAULT_ENCODING_ERROR_HANDLER,
    session_kwargs: dict[str, Any] | None = None,
) -> AsyncIterator[ClientSession]:
    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=env,
        cwd=cwd,
        encoding=encoding,
        encoding_error_handler=encoding_error_handler,
    )
    async with (
        _stdio_client(server_params, errlog=_devnull) as (read, write),
        ClientSession(read, write, **(session_kwargs or {})) as session,
    ):
        yield session


_lma_sessions._create_stdio_session = _quiet_create_stdio_session


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
