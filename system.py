from models.user import *
from utils.persistence import *
from utils.helper import *
from models.cartItem import *
from time import sleep



#create_table_products()
#create_table_users()


def main() -> None:
    loggedUser = None
    menu()

def menu(loggedUser = None) -> None:
    sleep(1)
    print('===================================')
    print('=========== Sistema Amazon ==========')
    print('===========Bem-vindo(a)  ==========')
    print('===================================')

    print('Selecione uma opção abaixo: ')
    print('1 - Cadastrar Usuário')
    print('2 - Listar usuários')
    print('3 - Realizar login de cliente')
    print('4 - Adicionar produto')
    print('5 - Editar produtos')
    print('6 - Deletar produtos')
    print('7 - Listar produtos')
    print('8 - Comprar produto')
    print('9 - Visualizar carrinho')
    print('10 - Remover item do carrinho')
    print('11 - Fechar pedido')
    print('12 - Adicionar saldo')
    print('13 - Logout')
    print('14 - Sair do sistema')

    op: int = int(input())

    if op == 1:
        register_user(loggedUser)
        menu(loggedUser)
    if op == 2:
        show_users(loggedUser)
        menu(loggedUser)
    elif op == 3:
        loggedUser = login(loggedUser)
        menu(loggedUser)
    elif op == 4:
        add_product(loggedUser)
        menu(loggedUser)
    elif op == 5:
        edit_products(loggedUser)
        menu(loggedUser)
    elif op == 6:
        remove_products(loggedUser)
        menu(loggedUser)
    elif op == 7:
        list_products()
        menu(loggedUser)
    elif op == 8:
        buy_products(loggedUser)
    elif op == 9:
        show_cart(loggedUser)
        menu(loggedUser)
    elif op == 10:
        remove_from_cart(loggedUser)
        menu(loggedUser)
    elif op == 11:
        close_order(loggedUser)
        menu(loggedUser)
    elif op == 12:
        payment(loggedUser)
        menu(loggedUser)
    elif op == 13:
        logout()
        menu()
    elif op == 14:
        logout()
        print('Volte sempre')
        exit(2)
    else:
        print('Opção não válida')
        menu(loggedUser)


def register_user(loggedUser):

    print("----Dados do cliente----")
    name = input("Informe nome do cliente: ")
    CPF = input("Informe CPF do cliente: ")
    email = input("Informe email do cliente: ")
    pwd = input("Informe a senha do cliente: ")

    if isUserLogged(loggedUser) and loggedUser.permission == 1:
        permission = input('Tipo de usuário: 1 - Admin 2-Cliente :')
        user = User(name, email, CPF, pwd, None, [], permission)

    user = User(name, email, CPF, pwd)
    add_user_db(user)


def show_users(loggedUser):
    if isUserLogged(loggedUser):
        if userHasPermission(loggedUser):
            list_users()


def login(loggedUser = None):
    if isUserLogged(loggedUser):
        print('Usuário já está logado')
        return loggedUser
    email = input("Digite o email: ")
    if '@' in email:
        pwd = input("Digite a senha: ")
        loggedUser = dao_login(email, pwd)
        if loggedUser == None:
            op1 = input("Deseja tentar novamente? Digite 1 para sim e qualquer tecla para não")
            if op1 == '1':
                login()
    else:
        print('Email invalido')
        login()
    return loggedUser


def add_product(loggedUser:User):
    if isUserLogged(loggedUser):
        if userHasPermission(loggedUser):
            productName = input('Informe o nome do produto: ')
            productPrice = float(input('Informe o preço: '))
            p = Product(productName, productPrice, get_number_of_products())
            add_product_db(p)


def edit_products(loggedUser):
    list_products()
    if isUserLogged(loggedUser):
        if userHasPermission(loggedUser):
            productCode = int(input('Informe o codigo do produto que deseja editar: '))
            if productCode in get_list_of_codes():
                productName= input('Informe o nome do produto: ')
                productPrice = float(input('Informe o preço: '))
                p = Product(productName, productPrice, productCode)
                update_delete_product_in_db(p, False)
            else:
                print('Produto não encontrado')


def remove_products(loggedUser):
    if isUserLogged(loggedUser):
        if userHasPermission(loggedUser):
            list_products()
            productCode = input('Informe o codigo do produto que deseja apagar: ')
            if int(productCode) in get_list_of_codes():
                p = get_product_by_code(productCode)
                print(p.name,' Removido ')
                update_delete_product_in_db(p, True)
            else:
                print('Produto não encontrado')


def buy_products(loggedUser):
    list_products()
    if isUserLogged(loggedUser):
        productCode = input('Informe o código dos produtos que deseja comprar: ')
        p = get_product_by_code(productCode)
        if p == None:
            print('Produto não encontrado. Deseja tentar novamente? Digite 1 para sim')
            op = input()
            if op == '1':
                buy_products(loggedUser)
        else:
            print(p)
            quantity = int(input('Informe quantas unidades deseja adcionar ao carrinho: '))
            totalPrice = (p.price*quantity)
            if loggedUser.hasLimit(totalPrice):
                print('Compra aprovada. O usuario possui limite')
                cartItem = CartItem(p, quantity)
                loggedUser.add_to_cart(cartItem)
                add_cart_item_db(loggedUser, cartItem)
            else:
                print('O usuario '+loggedUser.name+' não possui limite para tal compra')

    menu(loggedUser)


def show_cart(loggedUser):
    if isUserLogged(loggedUser):
        loggedUser.show_user_cart()


def remove_from_cart(loggedUser:User):
    if isUserLogged(loggedUser):
        show_cart(loggedUser)
        itemCode = int(input('Digite o código do item que deseja remover:'))
        itemQuantity = input('Informe quantas unidades deseja remover:')
        #cartItem = CartItem(get_product_by_code(itemCode),  )
        loggedUser.remove_item_from_cart(itemCode, itemQuantity)

        update_cart_item_in_db(loggedUser, itemCode)


def close_order(loggedUser: User):
    if isUserLogged(loggedUser):
        if len(loggedUser.cart) > 0:
            show_cart(loggedUser)
            op = input('Deseja fechar pedido? 1 para sim: ')
            if op == '1':
                loggedUser.purchase(loggedUser.cart_total())
                update_user_in_file(loggedUser)
                loggedUser.cart.clear()
                delete_cart_from_db(loggedUser)
                print('Compra realizada com sucesso!')
            else:
                return
        else:
            print('Carrinho está vazio')
    else:
        return



def payment(loggedUser):
    if isUserLogged(loggedUser):
        print('Saldo atual: ', formata_float_str_moeda(loggedUser.limit))
        payment = float(input("Informe quanto de saldo irá adicionar via boleto:"))
        loggedUser.limit += payment
        update_user_in_file(loggedUser)
        print('Saldo atual: ', formata_float_str_moeda(loggedUser.limit))


def logout():
    loggedUser = None


if __name__ == '__main__':
    main()