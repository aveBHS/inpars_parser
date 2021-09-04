import os
import cv2
import time
import traceback

import parse
from parse import *
from gdrive import GDrive
from config import config
from inpars import Inpars
from threading import Thread
from watermark import set_watermark


photos_buffer = {}


def photo_processing_thread(object_id, object_source, photo_url, photo_index):
    try:
        file_name = config("site.images_folder") + f'{object_id}_{photo_index}.jpg'
        with open(file_name, 'wb') as file:
            file.write(requests.get(photo_url).content)
        img = cv2.imread(file_name)
        img = set_watermark(img, object_source, config('source.logo.big'), config('source.logo.small'))
        cv2.imwrite(file_name, img)
        photos_buffer[object_id][photo_index] = [config("site.host") + config("site.images_path") + f'{object_id}_{photo_index}.jpg']
        photos_buffer[object_id][photo_index].append(photo_url)
    except:
        if config('debug'):
            traceback.print_exc()
        print(f"    [ERROR] Can't process image for ID{object_id}")
        try:
            if os.path.isfile(f'{object_id}_{photo_index}.jpg'):
                os.remove(f'{object_id}_{photo_index}.jpg')
        except:
            pass


if __name__ == '__main__':
    while True:
        print("[INFO] Inpars parser started")

        print("[ACTION] Connecting to DB")
        link = get_db_connection()
        if not link:
            print("[ERROR] Can't connect to DB")
            exit(1)
        print("[OK] Done")

        print("[ACTION] Loading local objects ids")
        local_objects = get_local_objects_ids()
        if local_objects is None:
            print("[ERROR] Can't get local objects")
            exit(1)
        print("[OK] Done")

        gdrive = GDrive()
        inpars = Inpars(config('inpars.credentials.api_key'))
        print("[ACTION] Starting update")
        while True:
            try:
                objects = inpars.get_objects()
            except:
                if config('debug'):
                    traceback.print_exc()
                print(f"    [ERROR] Can't get object list")
                time.sleep(10)
                continue
            if not objects:
                break

            for obj in objects:
                if int(obj['id']) in local_objects:
                    if not config('update'):
                        del local_objects[local_objects.index(int(obj['id']))]
                        print(f"    [OK] Object ID{obj['id']} skipped")
                        continue

                print(f" [ACTION] Processing pictures for object ID{obj['id']}")
                photo_processing_threads = []
                photos_buffer = {obj['id']: {}}
                if obj['images']:
                    for i, image in enumerate(obj['images']):
                        thread = Thread(target=photo_processing_thread, args=(obj['id'], obj['source'], image, i))
                        photo_processing_threads.append(thread)
                        thread.start()
                for thread in photo_processing_threads:
                    start_check_time = int(time.time())
                    while thread.is_alive():
                        if int(time.time()) - start_check_time > 30:
                            print("    [ERROR] Thread timeout, skip photo")
                            break
                unprocessed_photos = [i for i in obj['images']]
                for photo_id in photos_buffer[obj['id']].keys():
                    try:
                        obj['images'][photo_id] = photos_buffer[obj['id']][photo_id][0]
                        del unprocessed_photos[unprocessed_photos.index(photos_buffer[obj['id']][photo_id][1])]
                    except IndexError:
                        pass
                for photo in unprocessed_photos:
                    del obj['images'][obj['images'].index(photo)]
                photos_buffer = {}

                if int(obj['id']) in local_objects:
                    del local_objects[local_objects.index(int(obj['id']))]
                    if config('update'):
                        if update_object(obj, link):
                            print(f"    [OK] Object ID{obj['id']} created")
                        else:
                            print(f"    [ERROR] Can't update object ID{obj['id']}")
                    else:
                        print(f"    [OK] Object ID{obj['id']} skipped")
                else:
                    if create_object(obj, link):
                        print(f"    [OK] Object ID{obj['id']} created")
                    else:
                        print(f"    [ERROR] Can't create object ID{obj['id']}")

        print("[OK] Done")

        print(f"[INFO] Removed from publication: {len(local_objects)} objects")
        print("[ACTION] Archiving removed objects")
        for obj_id in local_objects:
            if archive_object(obj_id, link):
                print(f"    [OK] Object ID{obj_id} archived")
            else:
                print(f"    [ERROR] Can't archive object ID{obj_id}")
        print("[OK] Done")

        print("[ACTION] Setting update flag")
        parse.set_update_flag()
        print("[OK] Done")

        print('[INFO] All tasks done, restarting')
