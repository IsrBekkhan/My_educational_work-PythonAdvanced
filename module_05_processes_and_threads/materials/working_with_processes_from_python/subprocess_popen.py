import time
import subprocess


def run_program():
    start = time.time()
    procs = []
    for pnum in range(1, 6):
        p = subprocess.Popen(
            ['python', 'test_program.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print('Process number {} started. PID: {}'.format(
            pnum, p.pid
        ))
        procs.append(p)

    for proc in procs:
        proc.wait()
        if b'Done' in proc.stdout.read() and proc.returncode == 0:
            print('Process with PID {} ended successfully'.format(proc.pid))

    print('Done in {}'.format(time.time() - start))


if __name__ == '__main__':
    run_program()
