from aiohttp import ClientSession

from bot.config import bot_settings


class Client:
    def __init__(self):
        self._session: ClientSession | None = None

    def get_session(self):
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                base_url=bot_settings.api_url,
                raise_for_status=True,
            )
        return self._session


client = Client()
