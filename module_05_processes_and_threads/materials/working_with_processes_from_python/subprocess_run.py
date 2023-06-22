import subprocess


def run_program():
    res = subprocess.run(['python', 'test_program.py'], stdout=2)
    # res = subprocess.run(['python', 'test_program.py'])
    print(res)


if __name__ == '__main__':
    run_program()
