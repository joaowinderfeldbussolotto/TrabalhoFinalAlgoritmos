import csv
from utils.helper import formata_float_str_moeda
from utils.helper import error_code
from models.user import User
from models.product import Product
from models.cartItem import *

def create_file_users():
    with open(f'users.csv', 'w', newline='') as csvfile:
        fieldnames = ['Nome', 'CPF', 'Email', 'Senha','Limite','Permissão']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def create_file_products():
    with open(f'products.csv', 'w', newline='') as csvfile:
        fieldnames = ['Codigo', 'Nome', 'Preço']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def create_file_cart_items():
    with open(f'cart_items.csv', 'w', newline='') as csvfile:
        fieldnames = ['CPF','CódigoProduto','PreçoItem','Quantidade']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def add_cart_item_db(user: User,itemToBeAdd : CartItem):
    """
    Adiciona item do carrinho no arquivo cart_items.csv
    Caso o usuario esteja adicionando mais unidades de um item que ja comprou, invoca update_cart_item_in_db
    """
    for cartItem in user.cart:
        if cartItem.product.code == itemToBeAdd.product.code:
            update_cart_item_in_db(user,itemToBeAdd.product.code,False)
            return

    with open(f'cart_items.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        row = [user.cpf,itemToBeAdd.product.code, itemToBeAdd.itemPrice, itemToBeAdd.quantity]
        csv_writer.writerow(row)


def get_cart_by_cpf(cpf):
    #Agrupa todos itens(cart_items) associados a um cpf(parametro) e adiciona em um array de CartItems
    cart = []
    with open('cart_items.csv', 'r') as file_products:
        csv_file_reader = csv.DictReader(file_products)
        for row in csv_file_reader:
            if row['CPF'] == cpf:
                cartItem = CartItem(get_product_by_code(row['CódigoProduto']),row['Quantidade'])
                cart.append(cartItem)

    return cart


def update_cart_item_in_db(user:User, code, delete = False):
    lines = []
    with open('cart_items.csv', 'r') as productFile:
        csv_file_reader = csv.DictReader(productFile)
        for row in csv_file_reader:
            lines.append(row)
            if int(row['CódigoProduto']) == code and row['CPF'] == user.cpf:
                lines.remove(row)
    for item in user.cart:
        if item.product.code == code:
            lines.append({'CPF':user.cpf, 'CódigoProduto':code,'PreçoItem':item.itemPrice,'Quantidade':item.quantity })
    rewrite_cart_item_db(lines)


def delete_cart_from_db(user: User):
    lines = []
    with open('cart_items.csv', 'r') as productFile:
        csv_file_reader = csv.DictReader(productFile)
        for row in csv_file_reader:
            lines.append(row)
            if row['CPF'] == user.cpf:
                lines.remove(row)
    rewrite_cart_item_db(lines)


def rewrite_cart_item_db(alist):
    with open('cart_items.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(['CPF', 'CódigoProduto', 'PreçoItem', 'Quantidade'])
        for row in alist:
            i = [row['CPF'], row['CódigoProduto'], row['PreçoItem'], row['Quantidade']]
            writer.writerow(i)


def delete_cart_in_db(user: User):
    #Apaga todos itens do carrinho associados a um Usuario. Invocado quando usuário fecha o pedido.
    lines = []
    with open('cart_items.csv', 'r') as productFile:
        csv_file_reader = csv.DictReader(productFile)
        for row in csv_file_reader:
            lines.append(row)
            if row['CPF'] == user.cpf:
                lines.remove(row)
    with open('cart_items.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(['CPF','CódigoProduto','PreçoItem','Quantidade'])
        for row in lines:
            i = [row['CPF'], row['CódigoProduto'], row['PreçoItem'], row['Quantidade']]
            writer.writerow(i)


def get_list_of_codes():
    codes = []
    with open(f'products.csv','r') as productsFile:
        csv_file_reader = csv.DictReader(productsFile)
        for row in csv_file_reader:
            codes.append(int(row['Código']))
    return codes


def is_code_unique(code: int):
    codes = get_list_of_codes()
    if code in codes:
        return False

    return True


def get_number_of_products():
    rowCount = 0
    with open(f'products.csv', 'r') as productsFile:
        rowCount = sum(1 for row in productsFile)
    return rowCount


def add_product_db(product):
    with open(f'products.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        while not is_code_unique(product.code):
            product.code+=1
        row = [product.code, product.name, product.price]
        csv_writer.writerow(row)


def get_product_by_code(code):
    code = str(code)
    with open('products.csv', 'r') as file_products:
        csv_file_reader = csv.DictReader(file_products)
        for row in csv_file_reader:
            if row['Código'] == code:
                return Product(row['Nome'], float(row['Preço']), int(row['Código']))

    return None


def list_products():
    with open('products.csv', 'r') as file_products:
        csv_file_reader = csv.DictReader(file_products)
        for row in csv_file_reader:
            print(row['Código']+'. ' +row['Nome'] +': '+ formata_float_str_moeda(float(row['Preço'])))


def update_delete_product_in_db(product: Product, delete = False):
    #Função que atualiza ou deleta produto no arquivo .csv
    #Se delete == true, product não é sobrescrito no arquivo
    lines = []
    with open('products.csv', 'r') as productFile:
        csv_file_reader = csv.DictReader(productFile)
        for row in csv_file_reader:
            lines.append(row)
            if int(row['Código']) == product.code:
                lines.remove(row)

    with open('products.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(['Código', 'Nome', 'Preço'])
        for row in lines:
            i = [row['Código'], row['Nome'], row['Preço']]
            writer.writerow(i)
    if not delete:
        add_product_db(product)


def is_user_in_db(user):
    #Verifica existencia de email e cpf no sistema
    with open('users.csv', 'r') as _filehandler:
        csv_file_reader = csv.DictReader(_filehandler)
        for row in csv_file_reader:
            if row['Email'] == user.email or row['CPF'] == user.cpf:
                return True

    return False


def add_user_db(user):
    if not is_user_in_db(user):
        with open(f'users.csv', 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            row = [user.name, user.cpf, user.email, user.pwd, user.limit, user.permission]
            csv_writer.writerow(row)
    else:
        print("Usuario já cadastrado")
        return


def dao_login(email, pwd):
    #Acessa e verifica email e senha no arquivo
    #Caso deu certo, retorna o usuario(Classe User). Se não, retorna None
    loggedUser = None
    hasUser = False
    with open('users.csv', 'r') as u:
        csv_file_reader = csv.DictReader(u)
        for row in csv_file_reader:
            if row['Email'] == email:
                hasUser = True
                break

    if not hasUser:
        print(error_code(401))
        return

    else:
        with open('users.csv', 'r') as u:
            csv_file_reader = csv.DictReader(u)
            for row in csv_file_reader:
                if row['Email'] == email:
                    if row['Senha'] == pwd:
                        print(error_code(200))
                        loggedUser = User(row['Nome'], row['Email'],row['CPF'], row['Senha'], row['Limite'],
                                          get_cart_by_cpf(row['CPF']),
                                          row['Permissão'])

                    else:
                        print(error_code(403))
                        return
    return loggedUser


def update_user_in_file(user):
    lines = []
    with open('users.csv', 'r') as userFile:
        csv_file_reader = csv.DictReader(userFile)
        for row in csv_file_reader:
            lines.append(row)
            if row['CPF'] == user.cpf:
                lines.remove(row)

    with open('users.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(['Nome','CPF','Email','Senha','Limite','Permissão'])
        for row in lines:
            i = [row['Nome'], row['CPF'], row['Email'], row['Senha'], row['Limite'], row['Permissão']]
            writer.writerow(i)

    add_user_db(user)


def list_users():
    with open('users.csv', 'r') as usersFile:
        csv_file_reader = csv.DictReader(usersFile)
        for row in csv_file_reader:
            user = User(row['Nome'], row['Email'], row['CPF'],'******',row['Limite'],[],row['Permissão'])
            print(user)
            print()
