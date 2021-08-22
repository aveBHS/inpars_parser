import json
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
        return False


def update_object(obj: dict, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = link.cursor()

    sql = f'''
        UPDATE `{config('database.tables.objects')}` SET
            `title` = %s, `description` = %s, `lat` = %s, 
            `lng` = %s, `address` = %s, `cost` = %s, 
            `metroId` = %s, `phones` = %s, `floor` = %s, 
            `floors` = %s, `sq` = %s, `categoryId` = %s, `sectionId` = %s, 
            `typeAd` = %s, `cityId` = %s, `regionId` = %s
        WHERE `id` = %s;
    '''
    try:
        if cur.execute(sql, (
                obj['title'], obj['text'], obj['lat'],
                obj['lng'], obj['address'], obj['cost'],
                obj['metroId'], ','.join("{0}".format(n) for n in obj['phones']), obj['floor'],
                obj['floors'], obj['sq'], obj['categoryId'], obj['sectionId'],
                obj['typeAd'], obj['cityId'], obj['regionId'], obj['id']
        )) > 0:
            if obj['images']:
                sql = f'DELETE FROM {config("database.tables.images")} WHERE object_id = %s;'
                cur.execute(sql, obj['id'])

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
        return False


def archive_object(obj_id: int, link: pymysql.Connection = None):
    if not link:
        link = get_db_connection()
    cur = link.cursor()

    sql = f"UPDATE `{config('database.tables.objects')}` SET `status` = 1 WHERE `id` = %s;"
    try:
        result = cur.execute(sql, obj_id)
        link.commit()
        return result > 0
    except:
        if config('debug'):
            traceback.print_exc()
            print(cur._last_executed)
        return False


def get_local_objects_ids(cur: pymysql.connect.cursor = None):
    if not cur:
        link = get_db_connection()
        cur = link.cursor()

    try:
        cur.execute(f"SELECT `id` FROM {config('database.tables.objects')};")
        return [n[0] for n in cur.fetchall()]
    except:
        if config('debug'):
            traceback.print_exc()
        return None
