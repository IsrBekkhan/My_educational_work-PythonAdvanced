import time

def profiler(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        f = func(*args, **kwargs)
        after = time.time()
        print(after - before)

    return wrapper

@profiler
def hello_guys():
    print("Hello guys")

if __name__ == '__main__':
    hello_guys()
