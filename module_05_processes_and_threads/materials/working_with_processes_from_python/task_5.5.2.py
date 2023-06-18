import subprocess
import time


def sleeping():
    start = time.time()
    command = 'sleep 15 && echo "My mission is done here!"'
    processes = list()

    for _ in range(10):
        process = subprocess.Popen(command, shell=True)
        processes.append(process)

    for process in processes:
        process.wait()

        if process.returncode == 0:
            print('Process with PID {} ended successfully'.format(process.pid))

    print('Время работы программы {} сек.'.format(time.time() - start))


if __name__ == '__main__':
    sleeping()
