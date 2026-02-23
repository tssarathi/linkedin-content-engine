import re

GITHUB_URL_RE = re.compile(r"https://github\.com/\S+")


def parse_prompt(user_input: str) -> tuple[str, str | None]:
    match = GITHUB_URL_RE.search(user_input)
    if match:
        github_url = match.group(0)
        request = user_input.replace(github_url, "").strip()
        if not request:
            request = "Write a LinkedIn post showcasing this project"
        return request, github_url
    return user_input.strip(), None
