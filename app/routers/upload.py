from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from app.core.config import settings
from app.utils.dependencies import SessionDep

router = APIRouter(prefix="/upload", tags=["upload"])

api_key = settings.GOOGLE_API_KEY

if api_key is None:
	raise HTTPException(status_code=500, detail="GOOGLE_API_KEY environment variable is not set")

provider = GoogleProvider(api_key=api_key)
model = GoogleModel("gemini-2.0-flash", provider=provider)
agent = Agent(model)


@router.post("/")
async def upload_file(
	request: Request,
	session: SessionDep,
	file: Annotated[UploadFile, File(description="PDF resume file")],
):
	"""Upload a PDF file"""
	if not file:
		raise HTTPException(status_code=400, detail="No file uploaded")

	file_content = await file.read()
	result = await agent.run(
		[
			"Extract the full name of the resume owner. If multiple names are found, return the primary/main name. If no clear name is found, return 'Name not found'.",
			BinaryContent(data=file_content, media_type="application/pdf"),
		]
	)
	extracted_name = result.output.strip() if result.output else "Name not found"

	return {"success": "File uploaded successfully", "extracted_name": extracted_name}
