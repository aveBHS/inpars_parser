import json
import pymysql
import requests
import traceback
from config import config


def get_objects():
    url = "https://inpars.ru/api/v2/estate"
    headers = {
        "Accept": "application/json"
    }

    # Построение GET параметров запроса
    request_params = {'_format': 'json'}
    if config('credentials.api_key'):
        request_params['access-token'] = config('api_key')
    if config('regions'):
        request_params['regionId'] = ','.join("{0}".format(n) for n in config('regions'))

    if len(request_params) > 0:
        url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in request_params.items()])

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        objects = json.loads(response.text)
        print(objects)
    else:
        if config('debug'):
            traceback.print_exc()
        raise ValueError(f"Server response exception [{response.status_code}]")


if __name__ == '__main__':
    get_objects()
