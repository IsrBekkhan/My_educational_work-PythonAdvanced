class Cocktail:

    def do(self):
        pass


class Barman:

    def __init__(self):
        self.no_cocktails()

    def no_cocktails(self):
        self.cocktails = []

    def add_cocktail_order(self, cocktail):
        self.cocktails.append(cocktail)

    def do_cocktails(self):
        [cocktail.do() for cocktail in self.cocktails]
        self.no_cocktails()


def main():

    barman = Barman()
    for c in range(100):
        barman.add_cocktail_order(Cocktail())
    barman.do_cocktails()


if __name__ == '__main__':
    main()
