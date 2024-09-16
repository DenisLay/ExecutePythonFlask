import io
import sys
import json
import types

def execute_code(src):
    local_vars = {}
    error = None

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    pre_code = """
import importlib
import subprocess
import sys

logs = []

def import_package(name, package):
    try:
        logs.append('try to import module.')
        importlib.import_module(name)
        logs.append('module imported.')
    except ImportError as e:
        try:
            logs.append('ImportError.')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            logs.append('package installed.')
            importlib.import_module(name)
            logs.append('try to import.')
        except subprocess.CalledProcessError as e:
            logs.append('subprocess.CalledProcessError.')
            result = f'{str(e)} || exit 1'
            sys.exit(1)
        except ModuleNotFoundError as e:
            logs.append('ModuleNotFoundError.')
            result = f'{str(e)} || exit 2'
            sys.exit(2)
    """

    src = f'{pre_code}\n\n\n{src}'

    try:
        exec(src, globals(), local_vars)
    except Exception as e:
        error = str(e)
        return json.dumps({'error-first': f'{error} (RUNTIME)'})
    finally:
        sys.stdout = old_stdout

    output = new_stdout.getvalue()

    json_items = []
    for key, value in local_vars.items():
        if isinstance(value, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType)):
            json_value = str(type(value))
        else:
            try:
                json_value = json.dumps(value)
            except (TypeError, OverflowError):
                json_value = str(value)

        if key == 'result' or key == 'logs':
            json_items.append({'key': key, 'value': json_value})
        #json_items.append({'key': key, 'value': json_value})

    json_items.append({'key': 'src', 'value': src})

    result = json.dumps(json_items, indent=4)

    return result