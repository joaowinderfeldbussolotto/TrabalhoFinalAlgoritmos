from utils.helper import isCpfOk
from utils.helper import formata_float_str_moeda
from models.cartItem import *


# -*- coding: windows-1252 -*-

class User:

    def __init__(self, name, email, cpf, pwd, limit=None, cart=[], permission=2):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.pwd = pwd
        if limit == None:
            self.limit = 1000.00
            while not self.verify_user():
                pass
        else:
            self.limit = float(limit)
        self.cart = cart
        self.permission = int(permission)

    def verify_user(self):
        if '@' in self.email:
            if len(self.pwd) == 6:
                if isCpfOk(self.cpf):
                    print('Dados validos')
                    return True
                else:
                    self.cpf = input("CPF invalido\nDigite novamente: ")
                    return False
            else:
                self.pwd = input("Senha invalida\nDigite novamente: ")
                return False
        else:
            self.email = input("Email invalido\nDigite novamente:")
            return False

    def hasLimit(self, purchasePrice):
        if self.limit >= purchasePrice + self.cart_total():
            return True
        else:
            return False

    def purchase(self, purchasePrice):
        self.limit -= purchasePrice

    def add_to_cart(self, cartItem: CartItem):
        for item in self.cart:
            if item.product.code == cartItem.product.code:
                item.quantity += cartItem.quantity
                item.item_amount()
                return
        self.cart.append(cartItem)

    def cart_total(self):
        cart_total = 0.0
        for item in self.cart:
            cart_total += item.itemPrice
        return cart_total

    def remove_item_from_cart(self, code, quantity):
        code = int(code)
        quantity = int(quantity)
        flagProductFound = False

        for item in self.cart:
            if item.product.code == code:
                flagProductFound = True
                if item.quantity < quantity:
                    print('Foi requisitado remoção de %d itens, no entanto, estão cadastrados apenas %d desse produto.'
                          ' Todos os %d foram removidos' % (quantity, item.quantity, item.quantity))
                    self.cart.remove(item)
                elif item.quantity > quantity:
                    item.quantity -= quantity
                    item.item_amount()
                else:
                    self.cart.remove(item)
        if not flagProductFound:
            print('Produto não encontrado no carrinho')

    def show_user_cart(self):
        if len(self.cart) == 0:
            print('Carinho está vazio')
            return
        for item in self.cart:
            print(item)
        print('Total:', formata_float_str_moeda(self.cart_total()))

    def __str__(self):
        userString = f'Nome: {self.name}\nEmail: {self.email}\nCPF: {self.cpf}\nSenha: {self.pwd}\nLimite:{formata_float_str_moeda(self.limit)}\nTipo de Usuário : '
        if self.permission == 1:
            userString += 'Adminstrador'
        else:
            userString += 'Cliente'

        return userString
