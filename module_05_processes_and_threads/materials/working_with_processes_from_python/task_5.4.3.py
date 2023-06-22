import subprocess
import shlex


def processes_counter() -> int:
    command_str = 'ps -A'
    command = shlex.split(command_str)

    result = subprocess.run(command, capture_output=True)
    result_str = result.stdout.decode()
    processes_list = result_str.splitlines()[1:]

    return len(processes_list)


if __name__ == '__main__':
    print('Количество запущенных процессов:', processes_counter())
