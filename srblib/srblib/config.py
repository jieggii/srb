from betterconf import Config as BaseConfig
from betterconf import field
from betterconf.caster import to_int


class Config(BaseConfig):
    class Bot(BaseConfig):
        _prefix_ = "BOT"
        TOKEN = field()

    class Daemon(BaseConfig):
        _prefix_ = "DAEMON"
        PERIOD = field(caster=to_int)

    class Mongo(BaseConfig):
        _prefix_ = "MONGO"
        HOST = field()
        PORT = field(caster=to_int)
        DB_NAME = field()


config = Config()
