from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "unochapeco"

driver = GraphDatabase.driver(uri, auth=(user, password))

# Criação de nós Pessoa
query = """
CREATE
  (p1:Pessoa{id:5,
nome:"Marta",
datanasc:[10,10,2000], peso:54.80,
altura:1.58}),
  (p2:Pessoa{id:6,
nome:"Pedro", datanasc:[5,5,1980],
formacao:"Advogado",
cidade:"Curitiba", uf:"PR"});
"""
driver.execute_query(query)
print("Nós criados com sucesso!")
driver.close()

