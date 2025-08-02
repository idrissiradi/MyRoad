from datetime import timedelta

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.config import settings
from app.services.auth import authenticate_user, create_access_token, create_user
from app.utils.dependencies import CurrentUser, SessionDep, templates

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, current_user: CurrentUser):
	"""Registration page"""
	if current_user:
		return RedirectResponse(url="/dashboard", status_code=302)

	return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register_user(
	request: Request,
	session: SessionDep,
	full_name: str = Form(...),
	email: str = Form(...),
	password: str = Form(...),
	confirm_password: str = Form(...),
):
	"""Register a new user"""
	if password != confirm_password:
		return RedirectResponse(url="/register", status_code=302)

	# Create user with validation
	user, error = create_user(session, email, password, full_name)
	if not user:
		return templates.TemplateResponse(
			"auth/register.html", {"request": request, "error": error}, status_code=400
		)

	# Auto-login after successful registration
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)

	response = RedirectResponse(url="/dashboard", status_code=302)
	response.set_cookie(
		key="access_token",
		value=f"Bearer {access_token}",
		httponly=True,
		max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
		secure=False,
		samesite="lax",
		path="/",
	)
	return response


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, current_user: CurrentUser):
	"""Render the login page."""
	if current_user:
		return RedirectResponse(url="/dashboard", status_code=302)

	return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login_page(
	session: SessionDep,
	request: Request,
	email: str = Form(...),
	password: str = Form(...),
):
	"""Handle user login and set access token in cookies."""
	user = authenticate_user(session, email, password)
	if not user:
		return RedirectResponse(url="/login", status_code=302)

	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)

	response = RedirectResponse(url="/dashboard", status_code=302)
	response.set_cookie(
		key="access_token",
		value=f"Bearer {access_token}",
		httponly=True,
		max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
		secure=False,
		samesite="lax",
	)
	return response


@router.post("/logout")
async def logout():
	"""Handle user logout by clearing the access token cookie."""
	response = RedirectResponse(url="/", status_code=302)
	response.delete_cookie("access_token")
	return response
