#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

"""PEP 723 인라인 스크립트 의존성 예제.

이 스크립트는 별도의 pyproject.toml 없이 의존성을 선언한다.
uv run inline_script_example.py 로 실행하면 자동으로 의존성이 설치된다.
"""

import requests
from rich import print
from rich.panel import Panel

response = requests.get("https://api.github.com/repos/astral-sh/uv")
data = response.json()

panel = Panel(
    f"[bold]{data['full_name']}[/bold]\n"
    f"{data['description']}\n\n"
    f"⭐ Stars: {data['stargazers_count']:,}\n"
    f"🍴 Forks: {data['forks_count']:,}\n"
    f"📝 Language: {data['language']}",
    title="uv Repository Info",
)
print(panel)
