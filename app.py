from files_loader import Loader
from pprint import pprint

if __name__ == '__main__':
    path = r'C:\Users\Aleksandr\Downloads\files\files\73_2'
    loader = Loader(path)
    res = loader.load_from_directory()

    pprint(res)