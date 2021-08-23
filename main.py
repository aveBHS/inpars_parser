import os
import cv2
from parse import *
from gdrive import GDrive
from config import config
from inpars import Inpars
from watermark import set_watermark


if __name__ == '__main__':
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
        objects = inpars.get_objects()
        if not objects:
            break

        for obj in objects:

            print(f" [ACTION] Processing pictures for object ID{obj['id']}")
            if obj['images']:
                for i, image in enumerate(obj['images']):
                    with open("photo.jpg", 'wb') as file:
                        file.write(requests.get(image).content)
                    img = cv2.imread('photo.jpg')
                    img = set_watermark(img, obj['source'], config('source.logo.big'), config('source.logo.small'))
                    file_name = f'{obj["id"]}_{i}.jpg'
                    cv2.imwrite(file_name, img)
                    obj['images'][i] = gdrive.upload_image([{'name': file_name, 'file': file_name}])
                    os.remove(file_name)

            if obj['id'] in local_objects:
                del local_objects[local_objects.index(obj['id'])]
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
