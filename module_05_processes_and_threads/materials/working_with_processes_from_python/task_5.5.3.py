import subprocess


def sleep_exit():
    command = b'sleep 10 && exit 1'
    process = subprocess.Popen(command, shell=True)

    try:
        process.wait(timeout=9)
    except subprocess.TimeoutExpired:
        pass

    print(process.returncode)
    process.wait()
    print(process.returncode)


if __name__ == '__main__':
    sleep_exit()
