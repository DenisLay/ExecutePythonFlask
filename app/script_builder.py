import io
import sys
import json

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
    finally:
        sys.stdout = old_stdout

    output = new_stdout.getvalue()

    json_items = []
    for key, value in local_vars.items():
        json_items.append(dict(key=key, value=value))

    with open('db.txt', 'w') as f:
        f.write(json_items)

    result = json.dumps(json_items, indent=4)

    return result