import time
import json
import datetime
import requests
import traceback
from config import config
from datetime import datetime, timedelta


class Inpars:
    __slots__ = ('api_key', 'limit', 'queries',
                 'query_time', 'last_query', 'total_objects',
                 'rateRemaining', 'rateReset')

    def __init__(self, api_key: str, query_limit: int = 100):
        self.api_key = api_key
        self.limit = query_limit
        self.query_time = 0
        self.last_query = 0
        self.rateRemaining = 0
        self.rateReset = 0
        self.queries = 0
        self.total_objects = 0

    def limit_reset(self, query_limit: int = None):
        if query_limit:
            self.limit = query_limit
        self.query_time = 0
        self.queries = 0

    def get_objects(self):
        if self.query_time == -1:
            return None
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
        if config('inpars.cities'):
            request_params['cityId'] = ','.join("{0}".format(n) for n in config('inpars.cities'))
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

            query_date = datetime.fromisoformat(objects[-1]['updated'])
            last_month = (datetime.now() - timedelta(days=14)).timestamp()
            if query_date.timestamp() <= last_month:
                self.query_time = -1
            else:
                self.query_time = int(time.mktime(query_date.timetuple()))

            meta = response['meta']
            self.rateRemaining = meta['rateRemaining']
            self.rateReset = meta['rateReset']
            self.total_objects = meta['totalCount']

            return [obj for obj in objects if datetime.fromisoformat(obj['updated']).timestamp() > last_month]
        else:
            if response.status_code == 400:
                try:
                    response = json.loads(response.text)
                    if "Значение «timeEnd» не может быть меньше установленного по умолчанию значения «timeStart»." in response['message']:
                        return None
                except:
                    pass
            if config('debug'):
                traceback.print_exc()
            print(f"[ERROR_INFO] Request URL: {url}")
            raise ValueError(f"Server response exception [{response.status_code}]")

    def check_limits(self):
        if self.rateReset > 0 and self.rateRemaining < 1:
            if(int(time.time()) - self.last_query) < self.rateReset:
                time.sleep(self.rateReset - (int(time.time()) - self.last_query) + 1)


if __name__ == "__main__":
    api = Inpars(config("inpars.credentials.api_key"), config("inpars.request_limit"))
    while api.get_objects():
        pass
