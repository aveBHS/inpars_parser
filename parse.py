import json
import time
import pymysql
import requests
import traceback
from config import config


def get_db_connection():
    try:
        return pymysql.connect(
            host=config('database.credentials.host'),
            user=config('database.credentials.user'),
            password=config('database.credentials.password'),
            database=config('database.credentials.base')
        )
    except:
        if config('debug'):
            traceback.print_exc()
        return None


def get_cursor(link: pymysql.Connection):
    if not link:
        link = get_db_connection()
    cur = link.cursor()
    if cur.connection:
        return cur
    link = get_db_connection()
    return link.cursor()


def create_object(obj: dict, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = get_cursor(link)

    sql = f'''
        INSERT INTO `{config('database.tables.objects')}` (
            `inpars_id`, `title`, `description`, `lat`, 
            `lng`, `address`, `cost`, `name`,
            `metroId`, `phones`, `rooms`, `floor`, 
            `floors`, `sq`, `categoryId`, `sectionId`, 
            `typeAd`, `cityId`, `regionId`, 
            `source`, `metroSlug`, `materialSlug`, `origin`
        ) VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,  
            %s, %s, %s, %s, %s, 
            %s, %s, %s
        );
    '''
    try:
        if cur.execute(sql, (
                obj['id'], obj['title'], obj['text'], obj['lat'],
                obj['lng'], obj['address'], obj['cost'], obj['name'],
                obj['metroId'], ','.join("{0}".format(n) for n in obj['phones']), obj['rooms'],
                obj['floor'], obj['floors'], obj['sq'], obj['categoryId'], obj['sectionId'],
                obj['typeAd'], obj['cityId'], obj['regionId'],
                obj['source'], obj['metro'], obj['material'], obj['url']
        )) > 0:
            if obj['images']:
                for image in obj['images']:
                    sql = f'INSERT INTO {config("database.tables.images")} (`object_id`, `path`) VALUES ((SELECT `id` FROM `objects` WHERE `inpars_id` = %s), %s)'
                    cur.execute(sql, (obj['id'], image))
            link.commit()
            return True
        return False
    except:
        if config('debug'):
            traceback.print_exc()
            # print(cur._last_executed)
        return False
    finally:
        cur.close()


def update_object(obj: dict, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = get_cursor(link)

    sql = f'''
        UPDATE `{config('database.tables.objects')}` SET
            `title` = %s, `description` = %s, `lat` = %s, 
            `lng` = %s, `address` = %s, `cost` = %s, `name` = %s,
            `metroId` = %s, `phones` = %s, `floor` = %s, 
            `floors` = %s, `sq` = %s, `categoryId` = %s, `sectionId` = %s, 
            `typeAd` = %s, `cityId` = %s, `regionId` = %s, `rooms` = %s,
            `metroSlug` = %s, `materialSlug` = %s, `origin` = %s
        WHERE `inpars_id` = %s;
    '''
    try:
        if cur.execute(sql, (
                obj['title'], obj['text'], obj['lat'],
                obj['lng'], obj['address'], obj['cost'], obj['name'],
                obj['metroId'], ','.join("{0}".format(n) for n in obj['phones']), obj['floor'],
                obj['floors'], obj['sq'], obj['categoryId'], obj['sectionId'],
                obj['typeAd'], obj['cityId'], obj['regionId'], obj['rooms'],
                obj['metro'], obj['material'], obj['url'], obj['id']
        )) > 0:
            if obj['images']:
                sql = f'DELETE FROM {config("database.tables.images")} WHERE `object_id` = (SELECT `id` FROM `objects` WHERE `inpars_id` = %s);'
                cur.execute(sql, obj['id'])

                if obj['images']:
                    for image in obj['images']:
                        sql = f'INSERT INTO {config("database.tables.images")} (`object_id`, `path`) VALUES ((SELECT `id` FROM `objects` WHERE `inpars_id` = %s), %s)'
                        cur.execute(sql, (obj['id'], image))
            link.commit()
            return True
        return False
    except:
        if config('debug'):
            traceback.print_exc()
            print(json.dumps(cur._last_executed))
        return False
    finally:
        cur.close()


def archive_object(obj_id: int, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = get_cursor(link)

    sql = f"UPDATE `{config('database.tables.objects')}` SET `status` = 1 WHERE `inpars_id` = %s;"
    try:
        result = cur.execute(sql, obj_id)
        link.commit()
        return True
    except:
        if config('debug'):
            traceback.print_exc()
            print(cur._last_executed)
        return False
    finally:
        cur.close()


def archive_old_objects(date_from: str, status: int = 1, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = get_cursor(link)

    sql = f"UPDATE `{config('database.tables.objects')}` SET `status` = {status} WHERE `created` <= %s;"
    try:
        result = cur.execute(sql, date_from)
        link.commit()
        return True
    except:
        if config('debug'):
            traceback.print_exc()
            print(cur._last_executed)
        return False
    finally:
        cur.close()


def set_update_flag(link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = get_cursor(link)

    sql = f"UPDATE `updates` SET `time` = %s WHERE `type` = 'parser';"
    try:
        result = cur.execute(sql, int(time.time()))
        link.commit()
        return result > 0
    except:
        if config('debug'):
            traceback.print_exc()
            print(cur._last_executed)
        return False
    finally:
        cur.close()


def get_local_objects_ids(cur: pymysql.connect.cursor = None):
    if not cur:
        link = get_db_connection()
        cur = get_cursor(link)

    try:
        cur.execute(f"SELECT `inpars_id` FROM {config('database.tables.objects')} WHERE `inpars_id` > 0;")
        return [int(n[0]) for n in cur.fetchall()]
    except:
        if config('debug'):
            traceback.print_exc()
        return None
    finally:
        cur.close()
