# Created by: coderShan
# Created on: 2018/10/17


import config_default


class Dict(dict):
    def __init__(self, names=(), values=(), **kwargs):
        super().__init__(**kwargs)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % item)

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
    return r


def toDict(d):
    d = Dict()
    for k, v in d.items():
        d[k] = toDict(v) if isinstance(v, dict) else v
    return d


configs = config_default.configs

try:
    import config_override

    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
