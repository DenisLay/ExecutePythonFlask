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

    result = dict(local_vars=local_vars)

    return result