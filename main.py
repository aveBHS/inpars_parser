import traceback
from parse import *
from config import config
from inpars import Inpars


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
    if not local_objects:
        print("[ERROR] Can't get local objects")
        exit(1)
    print("[OK] Done")

    inpars = Inpars(config('inpars.credentials.api_key'))
    print("[ACTION] Starting update")
    while True:
        objects = inpars.get_objects()
        if not objects:
            break

        for obj in objects:

            # TODO image processing

            if obj['id'] in local_objects:
                update_object(obj, link)
                del local_objects[local_objects.index(obj['id'])]
            else:
                if create_object(obj, link):
                    print(f"[OK] Object ID{obj['id']} created")
                else:
                    print(f"[ERROR] Can't create object ID{obj['id']}")

    print("[OK] Done")

    print(f"[INFO] Removed from publication: {len(local_objects)} objects")
    print("[ACTION] Archiving removed objects")
    for obj_id in local_objects:
        if archive_object(obj_id, link):
            print(f"[OK] Object ID{obj_id} archived")
        else:
            print(f"[ERROR] Can't archive object ID{obj_id}")
    print("[OK] Done")
