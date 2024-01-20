from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta: 
    def __init__(self, agencia, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Operação inválida [saldo insuficiente]')

        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado!')
            return True
        
        else:
            print('Operação inválida [Valor informado inválido]')
    
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado')
        else:
            print('Operação inválida [Valor informado inválido]')
            return False

        return True
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )
    
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print('Operação inválida [valor maior do que o limite]')
        
        elif excedeu_saques:
            print('Operação inválida[Limite de saques atingido]')
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'''
            Agência: {self.agencia}
            CC:      {self.numero}
            Titular: {self.cliente.nome}
            '''


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.no().strftime('%d-%m-%Y %H:%M:%s'),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
    self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = f'''\n
            [1] Depositar
            [2] Sacar
            [3] Extrato
            [4] Nova conta
            [5] Listar contas
            [6] Novo Cliente
            [0] Sair
            Escolha uma opção>>> '''
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Não há conta vinculada a esse cliente')
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('informe o CPF do cliente >>> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    valor = float(input('Informe o valor do depósito>>> '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('informe o CPF do cliente >>> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    valor = float(input('Informe o valor do saque>>> '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def extrato():
    cpf = input('informe o CPF do cliente >>> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    
    print('Extrato>>>>>>>>>>>>>>\n')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram encontradas transações'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \tR${transacao['valor']:.2f}"

    print(extrato)
    print(f'\nSaldo: {conta.saldo:.2f}')

def nova_conta():
    cpf = input('informe o CPF do cliente >>> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Operação realizada com sucesso')

def listar_contas():
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))

def novo_cliente():
    cpf = input('informe o CPF do cliente >>> ')
    cliente = filtrar_cliente(cpf, clientes)

    if  cliente:
        print('Cliente já cadastrado')
        return
    
    nome = input('Nome completo >>> ')
    data_nascimento = input('Data de nascimento >>> ')
    endereco = input('Endereço >>> ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,endereco=endereco, cpf=cpf)

    clientes.append(cliente)

    print('Cadastro efetuado')

def sair():
    pass

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            extrato(clientes)

        elif opcao == '4':
            numero_conta = len(contas) + 1
            nova_conta(numero_conta, clientes, contas)

        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '6':
            novo_cliente(clientes)

        elif opcao == '0':
            sair()
            break
        
        else:
            print('Opção inválida - selecione uma opção válida')

if __name__ == '__main__':
    main()
