import json
import pymysql
import requests
import traceback
from config import config


def get_db_connection():
    return pymysql.connect(
        host=config('credentials.mysql.host'),
        user=config('credentials.mysql.user'),
        password=config('credentials.mysql.password'),
        database=config('credentials.mysql.base')
    )


def get_objects():
    url = "https://inpars.ru/api/v2/estate"
    headers = {
        "Accept": "application/json"
    }

    # Построение GET параметров запроса
    request_params = {'_format': 'json'}
    if config('credentials.api_key'):
        request_params['access-token'] = config('credentials.api_key')
    if config('regions'):
        request_params['regionId'] = ','.join("{0}".format(n) for n in config('regions'))

    if len(request_params) > 0:
        url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in request_params.items()])

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)['data']
    else:
        if config('debug'):
            traceback.print_exc()
        raise ValueError(f"Server response exception [{response.status_code}]")


def create_object(obj: dict, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = link.cursor()

    sql = f'''
        INSERT INTO `{config('database.tables.objects')}` (
            `id`, `title`, `description`, `lat`, 
            `lng`, `address`, `cost`, 
            `metroId`, `phones`, `floor`, 
            `floors`, `categoryId`, `sectionId`, 
            `typeAd`, `cityId`, `regionId`, 
            `source`
        ) VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,  
            %s, %s
        );
    '''
    try:
        if cur.execute(sql, (
            obj['id'], obj['title'], obj['text'], obj['lat'],
            obj['lng'], obj['address'], obj['cost'],
            obj['metroId'], ','.join("{0}".format(n) for n in obj['phones']), obj['floor'],
            obj['floors'], obj['categoryId'], obj['sectionId'],
            obj['typeAd'], obj['cityId'], obj['regionId'],
            obj['source']
        )) > 0:
            link.commit()
            return True
        return False
    except pymysql.err.ProgrammingError:
        if config('debug'):
            traceback.print_exc()
            print(cur._last_executed)
        else:
            print(f"[ERROR] Can't create new object ID{obj['id']}")
        return False


def get_local_objects_ids(cur: pymysql.connect.cursor = None):
    if not cur:
        link = get_db_connection()
        cur = link.cursor()

    cur.execute("SELECT `id` FROM `%s`;" % config('database.tables.objects'))
    result = cur.fetchall()
    print(result)


if __name__ == '__main__':
    get_objects()
