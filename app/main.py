import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.utils.dependencies import CurrentUser, templates

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=settings.openapi_url)


app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY, max_age=3600)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(auth_router, tags=["Authentication"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: CurrentUser):
	"""Render the home page."""
	if current_user:
		return RedirectResponse(url="/dashboard", status_code=302)
	return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: CurrentUser):
	if not current_user:
		# If the user is not authenticated, redirect to the login page.
		# This assumes you have a login route set up in your auth router.
		return RedirectResponse(url="/auth/login", status_code=302)
	return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
