import time
import json
import datetime
import requests
import traceback
from config import config


class Inpars:
    __slots__ = ('api_key', 'limit', 'queries',
                 'query_time', 'last_query', 'total_objects',
                 'rateRemaining', 'rateReset')

    def __init__(self, api_key: str, query_limit: int = 100):
        self.api_key = api_key
        self.limit = query_limit
        self.query_time = int(time.time())
        self.last_query = 0
        self.rateRemaining = 0
        self.rateReset = 0
        self.queries = 0
        self.total_objects = 0

    def limit_reset(self, query_limit: int = None):
        if query_limit:
            self.limit = query_limit
        self.query_time = int(time.time())
        self.queries = 0

    def get_objects(self):
        url = "https://inpars.ru/api/v2/estate"
        headers = {
            "Accept": "application/json"
        }

        # Построение GET параметров запроса
        request_params = {
            'access-token': self.api_key,
            '_format': 'json',
            'limit': self.limit,
            'expand': ','.join(config('inpars.expand_fields')),
            'timeEnd': self.query_time,
            'typeAd': ','.join("{0}".format(n) for n in config('inpars.typeAd')),
            'categoryId': ','.join("{0}".format(n) for n in config('inpars.categoryId'))
        }
        if config('inpars.regions'):
            request_params['regionId'] = ','.join("{0}".format(n) for n in config('inpars.regions'))
        if config('inpars.sources'):
            request_params['sourceId'] = ','.join("{0}".format(n) for n in config('inpars.sources'))

        if len(request_params) > 0:
            url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in request_params.items()])

        self.check_limits()  # Проверка лимитов перед запросом
        response = requests.get(url, headers=headers)
        self.queries += 1
        self.last_query = int(time.time())
        if response.status_code == 200:
            response = json.loads(response.text)
            objects = response['data']
            query_date = datetime.datetime.fromisoformat(objects[-1]['created'])
            self.query_time = int(time.mktime(query_date.timetuple()))

            meta = response['meta']
            self.rateRemaining = meta['rateRemaining']
            self.rateReset = meta['rateReset']
            self.total_objects = meta['totalCount']

            return objects
        else:
            if config('debug'):
                traceback.print_exc()
            raise ValueError(f"Server response exception [{response.status_code}]")

    def check_limits(self):
        if self.rateReset > 0 and self.rateRemaining < 1:
            if(int(time.time()) - self.last_query) < self.rateReset:
                time.sleep(self.rateReset - (int(time.time()) - self.last_query) + 1)
