from typing import Generator


# Example №1
# def gen_with_send() ->  Generator[None, int, None]:
#     while True:
#         item = yield
#         print(f"{item=}")
#
# g = gen_with_send()
# next(g)
# g.send(1)
# g.send(2)
# g.send(42)


# Example №2
# def gen_with_send() -> Generator[None, int, None]:
#     while True:
#         item = yield
#         print(f"{item=}")
#
# g = gen_with_send()
# g.send(None)
# g.send(1)
# g.send(2)
# g.send(42)


# Example №3
# def gen_with_send() -> Generator[None, int, str]:
#     while True:
#         item = yield
#         print(f"{item=}")
#         if item == 42:
#             return 'stopped'
#
# g = gen_with_send()
# g.send(None)
# g.send(1)
# g.send(2)
# g.send(42)


# Example №4
def gen_with_send() -> Generator[None, int, None]:
    item = 0
    while True:
        outer_item = yield item
        print(f"{item=}")
        print(f"{outer_item=}")
        item += 1


g = gen_with_send()
g.send(None)
g.send(42)
g.send(41)
