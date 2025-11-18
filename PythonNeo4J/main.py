from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "unochapeco"

driver = GraphDatabase.driver(uri, auth=(user, password))

def print_greeting(message):
    with driver.session() as session:
        greeting = session.run("RETURN $msg AS message", msg=message)
        for record in greeting:
            print(record["message"])

print_greeting("Conexão com Neo4j funcionando!")
driver.close()
