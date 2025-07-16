import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from app.core.database import get_session
from app.routers.auth import router as auth_router
from app.services.auth import get_current_user
from app.services.templates_config import templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(auth_router, tags=["Authentication"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session: Session = Depends(get_session)):
	user = get_current_user(request, session)
	if not user:
		return RedirectResponse(url="/auth/login", status_code=302)

	return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
