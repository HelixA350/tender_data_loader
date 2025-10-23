from files_loader import Loader

if __name__ == '__main__':
    path = r'C:\Users\Aleksandr\Downloads\files\files\73_2'
    loader = Loader(path)
    res = loader.load_from_directory()

    print(res)