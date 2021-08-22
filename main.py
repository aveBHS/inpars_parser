from parse import *
from config import config
from inpars import Inpars


if __name__ == '__main__':
    parser = Inpars(config('inpars.credentials.api_key'))
    print(parser.get_objects()[0]['text'])
    print(parser.get_objects()[0]['text'])
    print(parser.get_objects()[0]['text'])
