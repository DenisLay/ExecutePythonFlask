import io
import sys

def execute_code(src):
    local_vars = {}

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        exec(src, globals(), local_vars)
    except Exception as e:
        return {
            'error': str(e)
        }
    finally:
        sys.stdout = old_stdout

    result = new_stdout.getvalue()

    return {
        'error': None,
        'local_vars': local_vars,
        'result': result
    }