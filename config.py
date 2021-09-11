configs = {
    "debug": True,

    "update": True,
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
    "inpars": {
        "credentials": {
            "api_key": "HpwpTEwJdrCHNVUnF3Ppv_uqVVkA5vuJ"
        },
        "regions": [77],
        "cities": [1],
        "sources": [1, 2, 3, 5, 7, 9, 10, 11, 13, 15, 18, 20, 21],
        "expand_fields": ['rooms'],
        "typeAd": [1, 2],
        "categoryId": [28, 32, 47]
        # All sources: 1, 2, 3, 4, 5, 7, 9, 10, 11, 13, 15, 18, 19, 20, 21
    },
    "source": {
        "logo": {
            "big": "./sources/big.jpg",
            "small": "./sources/small.jpg"
        }
    },
    "gdrive": {
        "folder": "1ASAXw1GX5MaeJ1-S4xiA2r2dcm22QMIO"
    },
    "site": {
        "host": "example.com",
        "images_path": "/uploads/",
        "images_folder": "/var/www/site/public_html/uploads/",
        "default_photo": 'default.jpg'
    }
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
