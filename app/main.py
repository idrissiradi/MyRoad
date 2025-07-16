import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routers.auth import router as auth_router
from app.utils.dependencies import CurrentUser, SessionDep, templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(auth_router, tags=["Authentication"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: CurrentUser = None):
	"""Render the home page."""
	if current_user:
		return RedirectResponse(url="/dashboard", status_code=302)
	return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session: SessionDep, current_user: CurrentUser = None):
	if not current_user:
		return RedirectResponse(url="/auth/login", status_code=302)

	return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
