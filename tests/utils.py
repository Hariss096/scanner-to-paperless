# Taken from https://stackoverflow.com/a/59351425
class MockResponse:
    def __init__(self, text: str, status: int, headers: dict):
        self._text = text
        self.status = status
        self.headers = headers

    async def text(self):
        return self._text

    async def read(self):
        return self._text.encode()

    async def json(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
