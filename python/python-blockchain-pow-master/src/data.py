import os
import pathlib


def _ensure(path):
    if not os.path.exists(path):
        os.mkdir(path)


class DataFolder:
    folder = None
    common_sub = 'common'

    def __init__(self, folder):
        _ensure(folder)
        folder = self.folder = pathlib.Path(folder)
        _ensure(folder / self.common_sub)

    def sub_folder(self, sub_folder):
        _ensure(self.folder / sub_folder)


if __name__ == "__main__":
    data = DataFolder('data')
    data.sub_folder('5001')
