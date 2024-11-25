import sys

def print_user_message(*args):
    print(*args, file=sys.stderr)
