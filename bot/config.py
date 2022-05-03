from betterconf import Config as BaseConfig
from betterconf import field


class Config(BaseConfig):
    TOKEN = field()


config = Config()
