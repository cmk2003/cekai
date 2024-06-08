import os
import shutil
import subprocess
import sys
import tempfile

from cekai.settings import BASE_DIR

from test_runner import models
from test_runner.utils.fileLoader import FileLoader

EXEC = sys.executable

if 'uwsgi' in EXEC:
    EXEC = "/usr/bin/python"

def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')

class DebugCode(object):
    def __init__(self, code, project, filename):
        self.__code = code
        self.resp = None
        self.temp = tempfile.mkdtemp(prefix='tempHttpRunner', dir=os.path.join(BASE_DIR, 'tempWorkDir'))
        self.project = project
        self.filename = filename

    def run(self):
        # dumps file.py and run
        try:
            os.chdir(self.temp)
            files = models.Pycode.objects.filter(project__id=self.project)
            for file in files:
                file_path = os.path.join(self.temp, file.name)
                FileLoader.dump_python_file(file_path, file.code)

            run_file_path = os.path.join(self.temp, self.filename)
            self.resp = decode(subprocess.check_output([EXEC, run_file_path], stderr=subprocess.STDOUT, timeout=60))
        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)
        except subprocess.TimeoutExpired:
            self.resp = 'RunnerTimeOut'
        os.chdir(BASE_DIR)
        shutil.rmtree(self.temp)