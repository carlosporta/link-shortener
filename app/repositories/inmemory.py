from app.usecases.exceptions import AliasAlreadyExistsException


class InMemoryUrlRepository:
    def __init__(self):
        self._urls = {}

    def save(self, alias: str, url: str):
        if alias in self._urls:
            raise AliasAlreadyExistsException("Alias already exists")

        self._urls[alias] = url

    def get(self, alias: str) -> str | None:
        return self._urls.get(alias)
