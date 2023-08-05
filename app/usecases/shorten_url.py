from pydantic import BaseModel, HttpUrl, field_validator
from secrets import token_urlsafe

from app.repositories.inmemory import InMemoryUrlRepository
from app.usecases.exceptions import AliasNotFoundException


class ShortenRequest(BaseModel):
    url: HttpUrl
    alias: str | None = None

    @field_validator("url", mode="before")
    def prepend_https(cls, v):
        if isinstance(v, str) and not v.startswith("http"):
            return f"https://{v}"
        return v


class ShortenResponse(BaseModel):
    url: HttpUrl


class RedirectRequest(BaseModel):
    alias: str


class RedirectResponse(BaseModel):
    url: HttpUrl


def gen_token():
    return token_urlsafe()


def shorten(
    request: ShortenRequest,
    repo: InMemoryUrlRepository,
) -> ShortenResponse:
    alias = request.alias or gen_token()
    repo.save(alias, request.url)
    short_url = f"http://test/r/{alias}"
    return ShortenResponse(url=short_url)


def redirect(request: RedirectRequest, repo: InMemoryUrlRepository) -> RedirectResponse:
    url = repo.get(request.alias)
    if url is None:
        raise AliasNotFoundException()
    return RedirectResponse(url=url)
