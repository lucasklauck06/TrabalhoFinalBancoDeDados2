import psycopg2
import redis

# Funções para PostgreSQL

def connect_postgres():
    try:
        conn = psycopg2.connect(
            dbname="seu_banco", 
            user="seu_usuario", 
            password="sua_senha", 
            host="localhost", 
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar com PostgreSQL: {e}")
        return None

def create_postgres_user(name, email):
    conn = connect_postgres()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()

def read_postgres_user(user_id):
    conn = connect_postgres()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

def update_postgres_user(user_id, name, email):
    conn = connect_postgres()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        conn.commit()
        cursor.close()
        conn.close()

def delete_postgres_user(user_id):
    conn = connect_postgres()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

# Funções para Redis

def connect_redis():
    try:
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        return client
    except Exception as e:
        print(f"Erro ao conectar com Redis: {e}")
        return None

def create_redis_user(user_id, name, email):
    client = connect_redis()
    if client:
        client.hset(f"user:{user_id}", "name", name)
        client.hset(f"user:{user_id}", "email", email)

def read_redis_user(user_id):
    client = connect_redis()
    if client:
        user = client.hgetall(f"user:{user_id}")
        return user

def update_redis_user(user_id, name, email):
    client = connect_redis()
    if client:
        client.hset(f"user:{user_id}", "name", name)
        client.hset(f"user:{user_id}", "email", email)

def delete_redis_user(user_id):
    client = connect_redis()
    if client:
        client.delete(f"user:{user_id}")

# Exemplo de uso

# Operações com PostgreSQL
print("PostgreSQL CRUD:")
create_postgres_user("João", "joao@example.com")
user = read_postgres_user(1)
print("Usuário PostgreSQL:", user)
update_postgres_user(1, "João Silva", "joao.silva@example.com")
delete_postgres_user(1)

# Operações com Redis
print("\nRedis CRUD:")
create_redis_user(1, "Maria", "maria@example.com")
user_redis = read_redis_user(1)
print("Usuário Redis:", user_redis)
update_redis_user(1, "Maria Oliveira", "maria.oliveira@example.com")
delete_redis_user(1)
