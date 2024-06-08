import importlib
import shutil
import types
import yaml
import io
import json
import sys

def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function."""
    name, item = tup
    return isinstance(item, types.FunctionType)

def is_variable(tup):
    """ Takes (name, object) tuple, returns True if it is a variable."""
    name, item = tup
    if callable(item):
        # function or class
        return False
    if isinstance(item, types.ModuleType):
        # imported module
        return False
    if name.startswith("_"):
        # private property
        return False
    return True

class FileLoader(object):
    @staticmethod
    def dump_yaml_file(yaml_file, data):
        """ dump yaml file"""
        with io.open(yaml_file, 'w', encoding='utf-8') as stream:
            yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    @staticmethod
    def dump_json_file(json_file, data):
        """ dump json file"""
        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=4, separators=(',', ': '), ensure_ascii=False)

    @staticmethod
    def dump_python_file(python_file, data):
        """dump python file"""
        with io.open(python_file, 'a', encoding='utf-8') as stream:
            stream.write(data)

    @staticmethod
    def dump_binary_file(binary_file, data):
        """dump file"""
        with io.open(binary_file, 'wb') as stream:
            stream.write(data)

    @staticmethod
    def copy_file(path, to_path):
        """copy file to_path"""
        shutil.copyfile(path, to_path)

    @staticmethod
    def load_python_module(file_path):
        debugtalk_module = {
            "variables": {},
            "functions": {}
        }
        sys.path.insert(0, file_path)
        module = importlib.import_module("debugtalk")
        # 修复重载bug
        importlib.reload(module)
        sys.path.pop(0)
        for name, item in vars(module).items():
            if is_function((name, item)):
                debugtalk_module["functions"][name] = item
            elif is_variable((name, item)):
                if isinstance(item, tuple):
                    continue
                debugtalk_module["variables"][name] = item
            else:
                pass
        return debugtalk_module