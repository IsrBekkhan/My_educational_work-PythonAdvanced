from tasks import add

result = add.delay(4, 5)
print(repr(result))
print(result.get())
