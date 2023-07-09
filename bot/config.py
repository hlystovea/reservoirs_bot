from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str = ...
    api_url: str = 'https://reservoirs.hlystovea.ru'

    class Config:
        env_file = '../.env'


bot_settings = BotSettings()
