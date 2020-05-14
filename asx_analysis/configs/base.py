import attr


@attr.attrs()
class Config(object):
    api_key = attr.attrib(validator=attr.validators.instance_of(str), kw_only=True)


class Configuration(object):
    @classmethod
    def get_api_key(cls) -> str:
        raise NotImplementedError


__all__ = [
    "Configuration",
    "Config",
]
