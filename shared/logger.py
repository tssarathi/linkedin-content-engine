import logging
import os
from datetime import datetime

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

# Suppress noisy third-party loggers
for _name in ("langchain", "langchain_core", "langchain_community", "httpx", "httpcore"):
    logging.getLogger(_name).setLevel(logging.WARNING)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
