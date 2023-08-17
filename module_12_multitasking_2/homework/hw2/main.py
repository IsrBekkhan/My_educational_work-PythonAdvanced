from subprocess import run
import shlex


def process_count(username: str) -> int:
    command_str = f'ps U {username} -o ppid --no-headers | wc -l'
    process = run(command_str, shell=True, capture_output=True)

    if process.returncode == 0:
        result = int(process.stdout.decode()) - 1
        print(f'Количество запущенных процессов от пользователя {username}: {result}')

        return result


def total_memory_usage(root_pid: int) -> float:
    command_str = f'ps --ppid {root_pid} -o rss --sort -rss --no-headers'
    command = shlex.split(command_str)
    process = run(command, capture_output=True)

    if process.returncode == 0:
        memory_list = process.stdout.decode().splitlines()
        processes_sum = sum(map(int, memory_list))

        command_str = 'cat /proc/meminfo'
        command = shlex.split(command_str)
        process = run(command, capture_output=True)

        if process.returncode == 0:
            result = process.stdout.decode()
            total_ram = int(result.splitlines()[0].split()[1])
            using_ram = round((100 / total_ram) * processes_sum, 2)
            print(f'Использование оперативной памяти процессом с PID {root_pid}: {using_ram}%')

            return using_ram


if __name__ == '__main__':
    process_amount = process_count('bekkhan')
    process_size = total_memory_usage(1)
