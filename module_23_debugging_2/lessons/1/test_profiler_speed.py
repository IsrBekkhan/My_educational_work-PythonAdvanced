if __name__ == '__main__':
    import time

    start = time.time()

    len = 10000000
    my_list = []
    for c in range(len):
        my_list.append(c)

    finish = time.time()
    c = finish - start

    print(c)
