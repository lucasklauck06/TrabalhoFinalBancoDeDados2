import psycopg2

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


# Exemplo de uso

# Operações com PostgreSQL
print("PostgreSQL CRUD:")
create_postgres_user("João", "joao@example.com")
user = read_postgres_user(1)
print("Usuário PostgreSQL:", user)
update_postgres_user(1, "João Silva", "joao.silva@example.com")
delete_postgres_user(1)


