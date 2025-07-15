import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routers.auth import router as auth_router
from app.services.templates_config import templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(auth_router, tags=["Authentication"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
