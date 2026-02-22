import asyncio
import sys

from pipeline import run_pipeline


async def main():
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your prompt: ")
    post = await run_pipeline(user_input)
    print(post)


if __name__ == "__main__":
    asyncio.run(main())
