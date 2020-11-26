import subprocess

def print_log(*args):
    print(*args)

def run(args, **kwargs):
    print_log("+ '" + ' '.join(args) + "'")
    return subprocess.run(args, check=True, **kwargs)


def sudo_run(args, **kwargs):
    return run(['sudo', '-E'] + args, **kwargs)
