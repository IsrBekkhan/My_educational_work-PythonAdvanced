import subprocess


def processes_count():
    result = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.wait()
    result_list = result.stdout.readlines()

    return len(result_list[1:])


if __name__ == '__main__':
    count = processes_count()
    print('Количество запущенных процессов:', count)