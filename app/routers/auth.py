from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.services.templates_config import templates

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """
    Render the login page.
    """
    return templates.TemplateResponse("auth/login.html", {"request": request})
