from neo4j import GraphDatabase

# CONFIGURAÇÃO DO NEO4J
# Certifique-se de que seu banco Neo4j está rodando
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "unochapeco") # Altere para sua senha

class GrafoDB:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    # --- CRIAÇÃO DE NÓS (PESSOAS) ---
    def criar_pessoa(self, id_sql, cpf, nome):
        """
        Cria um nó Pessoa com id, cpf e nome conforme especificado.
        Usa MERGE para evitar duplicatas baseadas no CPF.
        """
        with self.driver.session() as session:
            query = """
            MERGE (p:Pessoa {cpf: $cpf})
            ON CREATE SET p.nome = $nome, p.id = $id_sql
            RETURN p.nome
            """
            result = session.run(query, cpf=cpf, nome=nome, id_sql=id_sql)
            return result.single()[0]

    # --- CRIAÇÃO DE RELACIONAMENTOS (AMIZADE) ---
    def adicionar_amizade(self, cpf_cliente, cpf_amigo):
        """
        Cria uma relação [:AMIGO_DE] entre dois nós existentes.
        """
        with self.driver.session() as session:
            # Verifica se ambos existem antes de criar a relação
            query = """
            MATCH (p1:Pessoa {cpf: $cpf1})
            MATCH (p2:Pessoa {cpf: $cpf2})
            MERGE (p1)-[:AMIGO_DE]->(p2)
            MERGE (p2)-[:AMIGO_DE]->(p1)  
            RETURN p1.nome, p2.nome
            """
            # Nota: A linha 'MERGE (p2)-[:AMIGO_DE]->(p1)' torna a amizade bidirecional.
            # Remova se a amizade for apenas num sentido (indicação única).
            
            result = session.run(query, cpf1=cpf_cliente, cpf2=cpf_amigo)
            if result.peek():
                print(f"✅ Amizade criada entre {cpf_cliente} e {cpf_amigo}")
            else:
                print("❌ Erro: Um ou ambos os CPFs não foram encontrados no grafo.")

    # --- CONSULTAS (LEITURA) ---
    def listar_amigos_de(self, cpf):
        with self.driver.session() as session:
            query = """
            MATCH (p:Pessoa {cpf: $cpf})-[:AMIGO_DE]-(amigo)
            RETURN amigo.nome, amigo.cpf
            """
            result = session.run(query, cpf=cpf)
            amigos = [record for record in result]
            return amigos

    def listar_todos(self):
        with self.driver.session() as session:
            query = "MATCH (p:Pessoa) RETURN p.id, p.nome, p.cpf"
            return list(session.run(query))

# --- MENU DE TESTE ---
def menu_grafo():
    # Inicializa conexão
    db = GrafoDB(URI, AUTH)

    while True:
        print("\n=== BASE 3: NEO4J (GRAFOS) ===")
        print("1. Adicionar Pessoa (Nó)")
        print("2. Adicionar Amizade (Relacionamento)")
        print("3. Listar Amigos de um Cliente")
        print("4. Listar Todas as Pessoas no Grafo")
        print("0. Sair")
        
        opcao = input("Opção: ")

        if opcao == '1':
            print("\n--- Adicionar Pessoa ---")
            # O ID aqui seria idealmente o mesmo gerado no PostgreSQL para manter consistência
            id_sql = int(input("ID (do Relacional/Sistema): ")) 
            cpf = input("CPF: ")
            nome = input("Nome: ")
            db.criar_pessoa(id_sql, cpf, nome)
            print("✅ Pessoa adicionada ao grafo.")

        elif opcao == '2':
            print("\n--- Criar Amizade ---")
            cpf1 = input("CPF do Cliente: ")
            cpf2 = input("CPF do Amigo: ")
            db.adicionar_amizade(cpf1, cpf2)

        elif opcao == '3':
            cpf = input("\nVer amigos do CPF: ")
            amigos = db.listar_amigos_de(cpf)
            if amigos:
                print(f"Amigos de {cpf}:")
                for amigo in amigos:
                    print(f"- {amigo['amigo.nome']} (CPF: {amigo['amigo.cpf']})")
            else:
                print("Nenhum amigo encontrado ou CPF inexistente.")

        elif opcao == '4':
            print("\n--- Pessoas no Grafo ---")
            pessoas = db.listar_todos()
            for p in pessoas:
                print(f"ID: {p['p.id']} | Nome: {p['p.nome']} | CPF: {p['p.cpf']}")

        elif opcao == '0':
            db.close()
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    try:
        menu_grafo()
    except Exception as e:
        print(f"Erro de conexão: {e}")
        print("Verifique se o Neo4j está rodando e se a senha está correta.")