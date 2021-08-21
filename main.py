from parse import *
from config import config


if __name__ == '__main__':
    i = 0
    for obj in get_objects():
        print(create_object(obj))
        i += 1
        if i == 10:
            break
