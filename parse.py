import json
import pymysql
import requests
import traceback
from config import config


def get_db_connection():
    return pymysql.connect(
        host=config('database.credentials.host'),
        user=config('database.credentials.user'),
        password=config('database.credentials.password'),
        database=config('database.credentials.base')
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
            `floors`, `sq`, `categoryId`, `sectionId`, 
            `typeAd`, `cityId`, `regionId`, 
            `source`
        ) VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,  
            %s, %s, %s
        );
    '''
    try:
        if cur.execute(sql, (
            obj['id'], obj['title'], obj['text'], obj['lat'],
            obj['lng'], obj['address'], obj['cost'],
            obj['metroId'], ','.join("{0}".format(n) for n in obj['phones']), obj['floor'],
            obj['floors'], obj['sq'], obj['categoryId'], obj['sectionId'],
            obj['typeAd'], obj['cityId'], obj['regionId'],
            obj['source']
        )) > 0:
            if obj['images']:
                for image in obj['images']:
                    sql = f'INSERT INTO {config("database.tables.images")} (`object_id`, `path`) VALUES (%s, %s)'
                    cur.execute(sql, (obj['id'], image))
            link.commit()
            return True
        return False
    except:
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

    cur.execute(f"SELECT `id` FROM {config('database.tables.objects')};")
    return [n[0] for n in cur.fetchall()]
