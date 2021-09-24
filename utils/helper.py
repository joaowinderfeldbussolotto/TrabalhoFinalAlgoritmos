# -*- coding: windows-1252 -*-



def digito_verificador(vetor):
    if sum(vetor) % 11 < 2:
        return 0
    else:
        return 11 - sum(vetor) % 11


def isCpfOk(cpf):
    cpf_test = [int(i) for i in cpf]

    if len(cpf_test) != 11:
        return False
    if cpf_test.count(cpf_test[0]) == len(cpf_test):
        return False
    else:
        cpf_test = cpf_test[:9]
        verificador = []
        aux = []
        j = 0
        for i in range(10, 1, -1):
            aux.append(cpf_test[j] * i)
            j += 1
        verificador.append(digito_verificador(aux))
        cpf_test.append(verificador[0])
        aux = []
        j = 0
        for i in range(11, 1, -1):
            aux.append(cpf_test[j] * i)
            j += 1
        verificador.append(digito_verificador(aux))
        cpf_test.append(verificador[1])

        for i in range(11):
            if int(cpf[i]) != cpf_test[i]:
                return False

        return True


def formata_float_str_moeda(valor) ->str:
  return f'R$ {valor:,.2f}'


def error_code(code):
    if code == 200:
        return 'Opera��o realizada com sucesso'
    if code == 401:
        return'Usu�rio n�o encontrado'
    if code == 403:
        return'Senha inv�lida'



def isUserLogged(user):
    if user == None:
        print('Usu�rio n�o est� logado')
        return False
    return True


def userHasPermission(user):
    if user.permission == 1:
        return True
    print('Usu�rio n�o tem permiss�o para tal opera��o')
    return False

