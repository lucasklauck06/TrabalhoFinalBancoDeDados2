# TrabalhoFinalBancoDeDados2
## Métodos principais do Driver
### driver.session()

Cria uma sessão (Session) para executar consultas no banco.

with driver.session(database="neo4j") as session:
    result = session.run("MATCH (n) RETURN n LIMIT 5")
    for record in result:
        print(record)


Uso comum: Criar sessões de leitura e escrita e executar queries com session.run().

### driver.verify_connectivity()

Verifica se o driver consegue se conectar ao servidor Neo4j.

try:
    driver.verify_connectivity()
    print("Conexão com o Neo4j bem-sucedida!")
except Exception as e:
    print("Erro de conexão:", e)


Uso: Diagnóstico — confirmar se as credenciais e a URI estão corretas.

### driver.execute_query(query, parameters=None, database=None, **kwargs)

Executa uma query diretamente, sem precisar abrir uma sessão manualmente.
(Disponível a partir do Neo4j Python Driver 5.x)

records, summary, keys = driver.execute_query(
    "MATCH (p:Person) RETURN p.name AS name LIMIT 5"
)

for record in records:
    print(record["name"])


Uso: Ideal para scripts simples e consultas diretas.

### driver.executable_query(query, parameters=None)

Cria uma query reutilizável (otimizada para múltiplas execuções).

query = driver.executable_query("MATCH (p:Person {name: $name}) RETURN p")
result = query.run(name="Alice")

for record in result:
    print(record["p"])


Uso: Queries otimizadas que podem ser reaproveitadas em várias sessões.

### driver.get_server_info()

Obtém informações sobre o servidor Neo4j conectado.

info = driver.get_server_info()
print("Versão do servidor:", info.agent)


Uso: Útil para logs e verificação de versão.

### driver.close()

Fecha o driver e libera os recursos usados.

driver.close()
