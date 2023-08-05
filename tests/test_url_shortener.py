from fastapi import status

from httpx import AsyncClient


async def test_should_shorten_an_url_successfully(
    async_client: AsyncClient,
):
    url_to_shorten = "github.com/carlosporta"
    response = await async_client.post(
        "/shorten",
        json={"url": url_to_shorten},
    )

    assert response.status_code == status.HTTP_201_CREATED
    url = response.json()["url"]
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    expected_location = f"https://{url_to_shorten}"
    assert response.headers["location"] == expected_location


async def test_should_shorten_an_url__wti_custom_alias_successfully(
    async_client: AsyncClient,
):
    url_to_shorten = "github.com/carlosporta"
    response = await async_client.post(
        "/shorten",
        json={"url": url_to_shorten},
    )

    assert response.status_code == status.HTTP_201_CREATED
    url = response.json()["url"]
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    expected_location = f"https://{url_to_shorten}"
    assert response.headers["location"] == expected_location


async def test_should_return_422_when_url_is_invalid(
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/shorten",
        json={"url": "invalid   url"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_should_return_404_when_alias_is_not_found(
    async_client: AsyncClient,
):
    response = await async_client.get("/not_found")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_should_not_register_an_alias_twice(
    async_client: AsyncClient,
):
    from app.api.routes import repo
    from app.usecases import shorten_url

    shorten_url.gen_token = lambda: "random_string"
    alias = "random_string"
    repo._urls = {alias: "https://github.com/carlosporta"}

    response = await async_client.post(
        "/shorten",
        json={"url": "https://google.com"},
    )
    assert response.status_code == status.HTTP_409_CONFLICT
