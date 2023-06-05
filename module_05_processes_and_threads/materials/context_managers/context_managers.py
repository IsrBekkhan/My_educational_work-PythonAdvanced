
def naive_approach():
    f = open('file.txt', 'w')
    f.write('Ping')
    f.close()


def try_finally_approach():
    f = open('file.txt', 'w')
    try:
        f.write('Ping')
    finally:
        f.close()


def with_approach():
    with('file.txt', 'w') as f:
        f.write('Ping')
