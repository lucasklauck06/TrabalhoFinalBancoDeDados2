import psycopg2
from psycopg2 import Error

# --- CONFIGURAÇÃO DA CONEXÃO ---
# Altere estes dados conforme o seu banco PostgreSQL local
DB_HOST = "localhost"
DB_NAME = "TrabalhoFinalBancoII" # Ex: trabalho_integracao
DB_USER = "postgres"
DB_PASS = "postgres"
DB_PORT = "5432"

def conectar():
    """Estabelece a conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

# ==========================================
# FUNÇÕES DE CLIENTES
# ==========================================
def criar_cliente(conn):
    print("\n--- Novo Cliente ---")
    cpf = input("CPF (apenas números): ")
    nome = input("Nome Completo: ")
    endereco = input("Endereço: ")
    cidade = input("Cidade: ")
    uf = input("UF (2 letras): ")
    email = input("E-mail: ")

    try:
        cursor = conn.cursor()
        sql = """INSERT INTO Clientes (cpf, nome, endereco, cidade, uf, email) 
                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
        cursor.execute(sql, (cpf, nome, endereco, cidade, uf, email))
        id_gerado = cursor.fetchone()[0]
        conn.commit()
        print(f"✅ Cliente cadastrado com sucesso! ID: {id_gerado}")
    except Error as e:
        print(f"❌ Erro ao inserir: {e}")

def listar_clientes(conn):
    print("\n--- Lista de Clientes ---")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, cpf, nome, email FROM Clientes ORDER BY id;")
        registros = cursor.fetchall()
        
        if not registros:
            print("Nenhum cliente encontrado.")
        else:
            print(f"{'ID':<5} {'CPF':<15} {'NOME':<30} {'EMAIL'}")
            print("-" * 70)
            for row in registros:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]}")
    except Error as e:
        print(f"❌ Erro ao ler dados: {e}")

def atualizar_cliente(conn):
    listar_clientes(conn)
    id_cliente = input("\nDigite o ID do cliente para atualizar: ")
    novo_nome = input("Novo Nome: ")
    novo_email = input("Novo E-mail: ")

    try:
        cursor = conn.cursor()
        sql = "UPDATE Clientes SET nome = %s, email = %s WHERE id = %s;"
        cursor.execute(sql, (novo_nome, novo_email, id_cliente))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Cliente atualizado!")
        else:
            print("⚠️ Cliente não encontrado.")
    except Error as e:
        print(f"❌ Erro ao atualizar: {e}")

def deletar_cliente(conn):
    listar_clientes(conn)
    id_cliente = input("\nDigite o ID do cliente para excluir: ")
    
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Clientes WHERE id = %s;"
        cursor.execute(sql, (id_cliente,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Cliente excluído!")
        else:
            print("⚠️ Cliente não encontrado.")
    except Error as e:
        print(f"❌ Erro ao excluir (verifique se há compras vinculadas): {e}")

# ==========================================
# FUNÇÕES DE PRODUTOS
# ==========================================
def criar_produto(conn):
    print("\n--- Novo Produto ---")
    produto = input("Nome do Produto: ")
    valor = float(input("Valor (ex: 10.50): "))
    quantidade = int(input("Quantidade em estoque: "))
    tipo = input("Tipo/Categoria: ")

    try:
        cursor = conn.cursor()
        sql = """INSERT INTO Produtos (produto, valor, quantidade, tipo) 
                 VALUES (%s, %s, %s, %s) RETURNING id;"""
        cursor.execute(sql, (produto, valor, quantidade, tipo))
        conn.commit()
        print("✅ Produto cadastrado com sucesso!")
    except Error as e:
        print(f"❌ Erro ao inserir produto: {e}")

def listar_produtos(conn):
    print("\n--- Estoque de Produtos ---")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, produto, valor, quantidade FROM Produtos ORDER BY id;")
        registros = cursor.fetchall()
        print(f"{'ID':<5} {'PRODUTO':<30} {'VALOR':<10} {'QTD'}")
        print("-" * 60)
        for row in registros:
            print(f"{row[0]:<5} {row[1]:<30} R${row[2]:<10} {row[3]}")
    except Error as e:
        print(f"❌ Erro: {e}")

# ==========================================
# FUNÇÕES DE COMPRAS (Relacionamento)
# ==========================================
def realizar_compra(conn):
    print("\n--- Nova Compra ---")
    listar_clientes(conn)
    id_cliente = input("Digite o ID do Cliente: ")
    
    listar_produtos(conn)
    id_produto = input("Digite o ID do Produto: ")

    try:
        cursor = conn.cursor()
        # Insere a compra usando a data padrão (DEFAULT CURRENT_TIMESTAMP) do banco
        sql = "INSERT INTO Compras (id_cliente, id_produto) VALUES (%s, %s);"
        cursor.execute(sql, (id_cliente, id_produto))
        conn.commit()
        print("✅ Compra registrada com sucesso!")
    except Error as e:
        print(f"❌ Erro ao registrar compra: {e}")

def listar_compras(conn):
    print("\n--- Relatório de Compras ---")
    try:
        cursor = conn.cursor()
        # Join para mostrar nomes em vez de apenas IDs
        sql = """
        SELECT c.id, cli.nome, p.produto, c.data 
        FROM Compras c
        JOIN Clientes cli ON c.id_cliente = cli.id
        JOIN Produtos p ON c.id_produto = p.id
        ORDER BY c.data DESC;
        """
        cursor.execute(sql)
        registros = cursor.fetchall()
        print(f"{'ID':<5} {'CLIENTE':<20} {'PRODUTO':<20} {'DATA'}")
        print("-" * 70)
        for row in registros:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20} {row[3]}")
    except Error as e:
        print(f"❌ Erro: {e}")

# ==========================================
# MENU PRINCIPAL
# ==========================================
def menu():
    conn = conectar()
    if not conn:
        return

    while True:
        print("\n=== GESTÃO BASE 1 (POSTGRESQL) ===")
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes")
        print("3. Atualizar Cliente")
        print("4. Excluir Cliente")
        print("----------------")
        print("5. Cadastrar Produto")
        print("6. Listar Produtos")
        print("----------------")
        print("7. Registrar Compra")
        print("8. Listar Compras")
        print("----------------")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1': criar_cliente(conn)
        elif opcao == '2': listar_clientes(conn)
        elif opcao == '3': atualizar_cliente(conn)
        elif opcao == '4': deletar_cliente(conn)
        elif opcao == '5': criar_produto(conn)
        elif opcao == '6': listar_produtos(conn)
        elif opcao == '7': realizar_compra(conn)
        elif opcao == '8': listar_compras(conn)
        elif opcao == '0': 
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

    conn.close()

if __name__ == "__main__":
    menu()