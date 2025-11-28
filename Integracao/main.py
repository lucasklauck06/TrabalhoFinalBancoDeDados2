import sys
# Importando os módulos que criamos (os arquivos devem estar na mesma pasta)
import db_postgres
import db_neo4j

# Configuração do Neo4j (Igual ao arquivo anterior)
URI_NEO4J = "bolt://localhost:7687"
AUTH_NEO4J = ("neo4j", "unochapeco") 

def fluxo_compra_integrada():
    print("\n=== NOVA COMPRA COM INDICAÇÃO (INTEGRAÇÃO) ===")
    
    # 1. Conectar ao PostgreSQL
    conn_pg = db_postgres.conectar()
    if not conn_pg:
        return

    try:
        # --- ETAPA 1: REALIZAR A COMPRA (RELACIONAL) ---
        # Listamos clientes para o usuário escolher quem está comprando
        db_postgres.listar_clientes(conn_pg)
        id_cliente = input("Digite o ID do Cliente que está comprando: ")
        
        # Precisamos pegar o CPF e Nome desse cliente para usar no Neo4j depois
        cursor = conn_pg.cursor()
        cursor.execute("SELECT cpf, nome FROM Clientes WHERE id = %s", (id_cliente,))
        dados_cliente = cursor.fetchone()
        
        if not dados_cliente:
            print("Cliente não encontrado.")
            return
            
        cpf_cliente, nome_cliente = dados_cliente

        # Listamos produtos e efetuamos a compra
        db_postgres.listar_produtos(conn_pg)
        id_produto = input("Digite o ID do Produto: ")
        
        # Função do db_postgres para registrar no banco relacional [cite: 10]
        # (Estou chamando direto o INSERT aqui para simplificar a integração)
        cursor.execute("INSERT INTO Compras (id_cliente, id_produto) VALUES (%s, %s)", (id_cliente, id_produto))
        conn_pg.commit()
        print("✅ Sucesso: Compra registrada no PostgreSQL (Base 1).")

        # --- ETAPA 2: INDICAR UM AMIGO (GRAFOS) ---
        print("\n--- INDICAÇÃO DE AMIGO ---")
        print("Conforme regra do sistema, indique um amigo para ganhar pontos.")
        
        # Conectar ao Neo4j
        grafo = db_neo4j.GrafoDB(URI_NEO4J, AUTH_NEO4J)
        
        cpf_amigo = input("CPF do Amigo indicado: ")
        nome_amigo = input("Nome do Amigo: ")

        # 1. Garante que o CLIENTE (quem comprou) existe no grafo
        grafo.criar_pessoa(id_sql=id_cliente, cpf=cpf_cliente, nome=nome_cliente)
        
        # 2. Cria o nó do AMIGO no grafo (Base 3) [cite: 16]
        # Nota: O amigo ainda não tem ID do Postgres pois não é cliente, passamos 0 ou None
        grafo.criar_pessoa(id_sql=0, cpf=cpf_amigo, nome=nome_amigo)
        
        # 3. Cria a relação de amizade
        grafo.adicionar_amizade(cpf_cliente, cpf_amigo)
        
        print("✅ Sucesso: Amizade registrada no Neo4j (Base 3).")
        grafo.close()

    except Exception as e:
        print(f"❌ Erro na integração: {e}")
    finally:
        if conn_pg:
            conn_pg.close()

def menu_principal():
    while True:
        print("\n=== SISTEMA INTEGRADOR DE VENDAS ===")
        print("1. Gerenciar PostgreSQL (Clientes/Produtos)")
        print("2. Gerenciar Neo4j (Visualizar Grafo)")
        print("3. REALIZAR COMPRA COMPLETA (Integração)")
        print("0. Sair")
        
        opcao = input("Opção: ")
        
        if opcao == '1':
            # Chama o menu do arquivo db_postgres.py
            db_postgres.menu() 
        elif opcao == '2':
            # Chama o menu do arquivo db_neo4j.py
            db_neo4j.menu_grafo()
        elif opcao == '3':
            fluxo_compra_integrada()
        elif opcao == '0':
            sys.exit()
        else:
            print("Inválido.")

if __name__ == "__main__":
    menu_principal()