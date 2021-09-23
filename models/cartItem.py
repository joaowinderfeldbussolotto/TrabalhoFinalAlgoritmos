from models.product import *
# -*- coding: windows-1252 -*-


class CartItem:
    def __init__(self, product: Product, quantity):
        self.product = product
        self.quantity = int(quantity)
        self.item_amount()

    def item_amount(self):
        self.itemPrice = self.product.price*self.quantity

    def __str__(self):
        return ('Codigo: %d Produto: %s Preco da unidade: %.2f Quantidade:%d Preco Item:%.2f'
                %(self.product.code,self.product.name, self.product.price,self.quantity,self.itemPrice))
