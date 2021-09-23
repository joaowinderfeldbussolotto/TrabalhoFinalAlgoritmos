from utils.helper import formata_float_str_moeda


class Product:

    count = 1

    def __init__(self, name, price, code = None):
        self.name  = name
        self.price = float(price)
        if code == None:
            Product.count += 1
            self.code = Product.count
        else:
            self.code = int(code)

    def __str__(self) -> str:
        return f'Código: {self.code}\nNome: {self.name} \nPreço: {formata_float_str_moeda(self.price)}'


