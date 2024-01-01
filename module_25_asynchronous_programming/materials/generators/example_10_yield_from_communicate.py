def sub_gen():
    val = yield
    print(f"{val=}")


def main_gen():
    gen = sub_gen()
    yield from gen

gen = main_gen()
gen.send(None)

gen.send('From main with love')