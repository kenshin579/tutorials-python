# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python tutorials and examples repository containing various Python code samples organized by topic. It serves as a learning reference with standalone examples.

## Project Structure

```
tutorials-python/
├── ai/                    # AI-related tutorials
│   ├── mcp/               # MCP (Model Context Protocol) examples
│   │   ├── hello_world/   # Basic FastMCP server/client
│   │   ├── weather/       # MCP weather server (pyproject.toml)
│   │   ├── fast_agent/    # FastAgent examples
│   │   └── ...
│   └── ollama/            # Ollama integration examples
├── python/                # Core Python tutorials
│   ├── argparse/          # Argparse examples (01-12)
│   ├── lambda/            # Lambda expressions with tests
│   ├── template_string/   # String template examples
│   └── third-party/       # Third-party library examples
│       ├── flask/         # Flask app with Docker
│       ├── google_drive_api/
│       ├── rate_limiting/ # aiolimiter, aiometer examples
│       └── web_scraping/  # BeautifulSoup, Tor examples
├── cloud/docker/          # Docker examples
└── blur-photo-sorter/     # Photo processing utility
```

## Running Code

### Individual Python Files
Most files are standalone scripts that can be run directly:
```bash
python python/argparse/01_argparse_basics.py
python ai/mcp/hello_world/server.py
```

### Running Tests
Tests use unittest framework:
```bash
python -m unittest python/lambda/test_lambda_expr.py
python -m unittest python/lambda/test_sort.py
```

### MCP Servers
```bash
# Using FastMCP CLI
fastmcp run ai/mcp/hello_world/server.py:mcp

# Or run directly
python ai/mcp/hello_world/server.py
```

### Flask App (Docker)
```bash
cd python/third-party/flask
make build && make run
# Or: ./run.sh
```

## Commit Message Format

All commit messages must be in Korean and follow this format:
```
[#이슈번호] <type>: <설명>

* 상세 설명 (필요시)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
[#3000] feat: 주식 가격 조회 API 구현

* REST API 엔드포인트 추가
* KIS API 연동
```

If no issue number exists, use branch name: `[chores] chore: 변경 설명`
