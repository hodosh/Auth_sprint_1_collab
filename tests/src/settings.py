from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')
    api_host: str = Field('http://127.0.0.1', env='AUTH_API_HOST')
    api_port: str = Field('8000', env='AUTH_API_PORT')

    def get_api_url(self):
        return f'{self.api_host}/{self.api_port}'.rstrip('/')


settings = TestSettings()
