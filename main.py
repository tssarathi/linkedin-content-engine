import subprocess
import threading
import time

from dotenv import load_dotenv

from app.utilities.logger import get_logger

logger = get_logger(__name__)

load_dotenv()


def run_backend():
    try:
        logger.info("Starting backend server")
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "8000"],
            check=True,
        )
    except Exception as e:
        logger.error("Problem with backend service")
        raise Exception(f"Problem with backend service: {e}")


def run_frontend():
    try:
        logger.info("Starting frontend server")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except Exception as e:
        logger.error("Problem with frontend service")
        raise Exception(f"Problem with frontend service: {e}")


def main():
    try:
        logger.info("Starting the application")
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()

    except Exception as e:
        logger.exception(f"Exception occured: {e}")


if __name__ == "__main__":
    main()
