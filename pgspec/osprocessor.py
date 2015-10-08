import os

class OsProcessor:
    root_path = ""
    last_path = ""
    origin = ""

    def __init__(self, root_path):
        self.root_path = root_path
        self.origin = os.getcwd()

    def file_exists(self, filename):
        return os.path.isfile(self.root_path + "/" + filename) == True;

    def change_to_root(self):
        self.last_path = os.getcwd()
        os.chdir(self.root_path)

    def change_dir(self, directory):
        self.last_path = os.getcwd()
        os.chdir(self.root_path + directory)

    def return_to_origin(self):
        return os.chdir(self.origin)
