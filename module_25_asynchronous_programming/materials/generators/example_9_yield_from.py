# def sub_gen():
#     for i in range(5):
#         yield i
# >>>


def sub_gen():
    yield from range(5)


# def main_gen():
#     gen = sub_gen()
#     for i in gen:
#         yield i
# >>>


def main_gen():
    gen = sub_gen()
    yield from gen


gen = main_gen()
for i in gen:
    print(i)