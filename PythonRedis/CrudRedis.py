import redis

r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True  # para retornar strings ao invés de bytes
)

def criar(chave, valor):
    if r.exists(chave):
        print(f"A chave '{chave}' já existe.")
    else:
        r.set(chave, valor)
        print(f"Chave '{chave}' criada com valor '{valor}'.")

def ler(chave):
    valor = r.get(chave)
    if valor:
        print(f"Valor da chave '{chave}': {valor}")
    else:
        print(f"Chave '{chave}' não encontrada.")

def atualizar(chave, novo_valor):
    if r.exists(chave):
        r.set(chave, novo_valor)
        print(f"Chave '{chave}' atualizada para '{novo_valor}'.")
    else:
        print(f"Chave '{chave}' não existe para atualizar.")

def deletar(chave):
    if r.exists(chave):
        r.delete(chave)
        print(f"Chave '{chave}' excluída.")
    else:
        print(f"Chave '{chave}' não encontrada para exclusão.")

def menu():
    while True:
        print("\n--- MENU CRUD REDIS ---")
        print("1. Criar")
        print("2. Ler")
        print("3. Atualizar")
        print("4. Deletar")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            chave = input("Informe a chave: ")
            valor = input("Informe o valor: ")
            criar(chave, valor)
        elif opcao == '2':
            chave = input("Informe a chave para consulta: ")
            ler(chave)
        elif opcao == '3':
            chave = input("Informe a chave a ser atualizada: ")
            novo_valor = input("Novo valor: ")
            atualizar(chave, novo_valor)
        elif opcao == '4':
            chave = input("Informe a chave a ser deletada: ")
            deletar(chave)
        elif opcao == '5':
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    try:
        # Testa a conexão
        r.ping()
        print("Conectado ao Redis com sucesso!")
        menu()
    except redis.ConnectionError:
        print("Não foi possível conectar ao Redis. Verifique se o servidor está em execução.")