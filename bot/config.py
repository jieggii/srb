from betterconf import Config as BaseConfig
from betterconf import field
from betterconf.caster import to_int


class Config(BaseConfig):
    TOKEN = field()

    class Mongo(BaseConfig):
        _prefix_ = "MONGO"
        HOST = field()
        PORT = field(caster=to_int)
        DB_NAME = field()


config = Config()
