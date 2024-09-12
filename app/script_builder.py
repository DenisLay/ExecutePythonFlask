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
            json_value = str(type(value)).encode('utf-8').decode('unicode_escape')
        else:
            try:
                json_value = json.dumps(value)
            except (TypeError, OverflowError):
                json_value = str(value)

        if key == 'result':
            json_items.append({'key': key, 'value': json_value})
        #json_items.append({'key': key, 'value': json_value})

    result = json.dumps(json_items, indent=4)

    return result