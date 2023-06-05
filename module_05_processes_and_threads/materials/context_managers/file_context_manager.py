import contextlib


class SavedFile:
    def __init__(self, path: str, mode='r'):
        self.name = path
        self.mode = mode

    def __enter__(self):
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, type, value, traceback):
        print("Exception {} has been handled".format(type))
        self.file.close()
        return True


if __name__ == '__main__':
    with SavedFile('some', 'w') as f:
        f.undefined('hello')
