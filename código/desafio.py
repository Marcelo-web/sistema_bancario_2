import textwrap

def menu():
   menu = """
    ================ MENU ==================
    [nu]\tCriar usuário
    [nc]\tCriar conta
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [lc]\tListar contas
    [q]\tSair
    => """
   return input(textwrap.dedent(menu))

 
def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
         saldo += valor_deposito
         extrato += f"Depósito:\tR$ {valor_deposito:.2f}\n" 
         formata_mensagem("Depósito realizado com sucesso!")  
    else:
        print(">>> Falha na operação! Valor de depósito inválido! <<<")
    
    return saldo, extrato


def sacar(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo =  valor_saque > saldo
    excedeu_limite = valor_saque > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print(">>> Operação falhou! Não há saldo suficiente! <<<")
    elif excedeu_limite:
        print(">>> Operação falhou! Valor do saque excede o limite! <<<")
    elif excedeu_saques:
        print(">>> Operação falhou! Número máximo de saques excedido! <<<")
    elif valor_saque > 0:
        saldo -= valor_saque
        numero_saques += 1
        extrato += f"Saque:\t\tR$ {valor_saque:.2f}\n"  
        formata_mensagem("Saque realizado com sucesso!")
    else:
        print(">>> Falha na operação! Valor de saque inválido! <<<") 
    
    return saldo, extrato, numero_saques   
 
 
def exibir_extrato(saldo, /, *, extrato):
    print()
    print(" extrato ".upper().center(40, '='))
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"Saldo:\t\tR$ {saldo:.2f}")
    print('=' * 40)
    

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if cpf in usuario["cpf"]:
            return usuario
    return None


def criar_usuario(usuarios):   
    cpf = input("Insira o seu CPF (somente números): ")  
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("<<< Falha na operação! Já existe usuário com esse CPF! >>>")
        return
    
    nome = input("Insira o seu nome: ")
    nascimento = input("Insira sua data de nascimento (dd/MM/YYYY): ")
    logradouro = input("Insira seu logradouro: ")
    numero = input("Insira o seu número: ")
    bairro = input("Insira o seu bairro: ")
    cidade = input("Insira sua cidade: ")
    sigla = input("Insira a sigla de seu Estado: ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{sigla}"
    
    usuario = {}
    chaves  = ["nome", "cpf", "nascimento", "endereco"]
    valores = [nome, cpf, nascimento, endereco]
    
    for chave, valor in zip(chaves, valores):
        usuario[chave] = valor
           
    usuarios.append(usuario)
    formata_mensagem("Usuário criado com sucesso!")
   

def criar_conta(agencia, numero_conta, usuarios): 
    cpf = input("Insira o seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios) 
    
    if not usuario:
        print("<<< Falha na operação! Usuário NÃO encontrado! >>>")
        return
    
    conta = {}
    conta.setdefault("agencia", agencia)
    conta.setdefault("numero_conta", numero_conta)
    conta.setdefault("usuario", usuario)
    
    formata_mensagem("Conta criada com sucesso!")
    return conta
    

def listar_contas(contas):
    print()
    print(f" Lista de contas bancárias ".center(40, '*'))  
    for conta in contas:
        titular = conta["usuario"]["nome"]
        numero_conta = conta["numero_conta"]
        agencia = conta["agencia"]
        resultado = f"""
            Agência:\t{agencia}
            C/C:\t\t{numero_conta}
            Titular:\t{titular}
        """
        print(textwrap.dedent(resultado))
    print("*" * 40)
    print()

  
def formata_mensagem(texto):
    texto = str(texto) 
    texto_centralizado = texto.center(40, ' ')
    print()
    print("|" + "-" * (40) + "|")
    print("|" + texto_centralizado +  "|")
    print("|" + "-" * (40) + "|")
        
       
def main():   
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
        
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == "d":
            valor_deposito = float(input("Valor para depósito: "))
            saldo, extrato = depositar(saldo, valor_deposito, extrato)
            
        elif opcao == "s":
            valor_saque = float(input("Informe o valor de saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                valor_saque=valor_saque,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
              
        elif opcao == "nu":
            criar_usuario(usuarios=usuarios)
            
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)  
            if conta:
                contas.append(conta) 
                
        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == "q":
            confirmacao = input("Deseja realmente sair da aplicação? [1-sair ou 2-continuar]: ")
            while confirmacao != "1" and confirmacao != "2":
                print("Opção inválida!")
                confirmacao = input("Deseja realmente sair da aplicação? [1-sair ou 2-continuar]: ")
            if confirmacao == "1":
                break
            elif confirmacao == "2":
                continue
            
        else:
            print("<<< Operação inválida, por favor selecione novamente a operação desejada. >>>") 
            
main()