import os

__PID_FILE__ = "pgspec.pid"

class OsProcessor:
    root_path = ""
    last_path = ""
    origin = ""
    pid = None

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

    def start_pid(self):
        if self.file_exists(__PID_FILE__):
            return False

        self.pid = os.getpgid(0)
        cur = os.getcwd()
        os.chdir(self.root_path)
        fo = open(__PID_FILE__, "w")
        fo.write(str(self.pid))
        fo.close()
        os.chdir(cur)
        return True

    def end_pid(self):
        cur = os.getcwd()
        os.chdir(self.root_path)
        self.pid = None
        if os.path.isfile(self.root_path + "/" + __PID_FILE__):
            os.remove(__PID_FILE__)

        os.chdir(cur)
