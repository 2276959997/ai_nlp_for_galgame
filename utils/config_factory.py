from utils.config_from_ini import ConfigFromIni


class GetConfig:

    @classmethod
    def get_config(cls, name='ini_config'):
        if name == "ini_config":
            return ConfigFromIni()