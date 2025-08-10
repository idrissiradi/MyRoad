# MyRoad

MyRoad is a Python web project.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [Jinja](https://jinja.palletsprojects.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [uv](https://github.com/uv-org/uv)
- [Tailwind CSS](https://tailwindcss.com/)
- [Alpine.js](https://alpinejs.dev/)
- [htmx](https://htmx.org/)
- [Pydantic AI](https://github.com/pydantic/pydantic-ai)
- [Gemini (Google AI)](https://ai.google.dev/)

## Development

This project uses [uv](https://github.com/uv-org/uv) for creating virtual environments and managing dependencies.

### Setup

```bash
uv venv .venv
source .venv/bin/activate
```

### Running

Start Tailwind CSS watcher (in one terminal):

```bash
bunx @tailwindcss/cli -i ./app/static/css/input.css -o ./app/static/css/output.css --watch
```

Start FastAPI server (in another terminal):

```bash
uv run fastapi dev app/main.py
```

## License

This project is licensed under the MIT License.
