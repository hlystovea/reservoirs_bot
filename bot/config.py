from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str = ...
    api_url: AnyHttpUrl = 'https://reservoirs.hlystovea.ru/'
    api_token: str = ...

    class Config:
        env_file = '../.env'


bot_settings = BotSettings()
