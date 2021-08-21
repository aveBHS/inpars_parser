configs = {
    "debug": True,
    "credentials": {
        "api_key": "HpwpTEwJdrCHNVUnF3Ppv_uqVVkA5vuJ"
    },
    "database": {
        "credentials": {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "base": "inpars"
        },
        "tables": {
            "objects": "objects",
            "images": "images"
        }
    },
    "regions": [77]
}


def config(param):
    try:
        value = None
        for route in param.split("."):
            if route in configs.keys() or value and route in value.keys():
                if value is not None:
                    value = value[route]
                else:
                    value = configs[route]
            else:
                return None
        if value:
            return value
        return None
    except TypeError:
        return None
