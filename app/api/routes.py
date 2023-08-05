from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from app.usecases import shorten_url as shorten_url_usecase
from app.usecases.exceptions import AliasAlreadyExistsException, AliasNotFoundException


router = APIRouter()
repo = shorten_url_usecase.InMemoryUrlRepository()


@router.post(
    "/shorten",
    status_code=status.HTTP_201_CREATED,
    response_model=shorten_url_usecase.ShortenResponse,
)
async def shorten_url(schema: shorten_url_usecase.ShortenRequest):
    try:
        url = shorten_url_usecase.shorten(schema, repo=repo)
    except AliasAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Alias already exists",
        )
    return url


@router.get("/r/{alias}")
async def redirect(alias: str):
    redirect_request = shorten_url_usecase.RedirectRequest(alias=alias)

    try:
        usecase_response = shorten_url_usecase.redirect(redirect_request, repo=repo)
    except AliasNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    return RedirectResponse(usecase_response.url)


@router.get("/health")
async def health():
    return {"status": "ok"}
