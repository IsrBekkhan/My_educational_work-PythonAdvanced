import subprocess
import shlex


def close_gunicorn():
    get_pids = 'ps -A'
    get_pids_command = shlex.split(get_pids)
    pids = subprocess.run(get_pids_command, capture_output=True)
    pids_str = pids.stdout.decode()

    gunicorn_pids = [line.split()[0] for line in pids_str.split('\n') if 'gunicorn' in line]

    for pid in gunicorn_pids:
        kill_pid = f'kill -15 {pid}'
        kill_pid_command = shlex.split(kill_pid)
        subprocess.run(kill_pid_command)

