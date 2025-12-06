import redis
import json
import db_postgres  # <--- IMPORTADO para listar clientes

# CONFIGURAÇÃO REDIS
# Padrão: localhost, porta 6379
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def testar_conexao_redis():
    """Verifica se o Redis está acessível."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2)
        r.ping()
        return True
    except Exception:
        return False

def conectar_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# --- FUNÇÕES DE CACHE ---
def salvar_recomendacao(cpf_alvo, dados_consolidados):
    """
    Salva o JSON consolidado (Compras + Amigos + Interesses).
    Define expiração de 1 hora (3600s) para simular cache.
    """
    r = conectar_redis()
    chave = f"recomendacao:{cpf_alvo}"
    
    # Serializa o dicionário Python para String JSON
    valor_json = json.dumps(dados_consolidados, indent=4, ensure_ascii=False)
    
    r.set(chave, valor_json, ex=3600) 
    print(f"✅ Dados consolidados salvos no Redis para o CPF {cpf_alvo}")

def buscar_recomendacao(cpf_alvo):
    """Retorna os dados do Redis se existirem."""
    r = conectar_redis()
    chave = f"recomendacao:{cpf_alvo}"
    
    dados_json = r.get(chave)
    if dados_json:
        return json.loads(dados_json) # Retorna como dicionário
    return None

def limpar_cache():
    """Limpa todas as chaves (usado para recarregar dados)"""
    r = conectar_redis()
    r.flushdb()
    print("🧹 Cache do Redis foi limpo.")

# --- MENU DE TESTE ---
def menu_redis():
    while True:
        print("\n=== BASE 4: REDIS (CACHE/CONSULTA) ===")
        print("1. Buscar Recomendação por CPF")
        print("2. Limpar Cache")
        print("0. Voltar")
        
        op = input("Opção: ")
        
        if op == '1':
            # --- MUDANÇA AQUI: LISTAR CLIENTES DO POSTGRES ---
            print("\n--- Clientes Disponíveis para Consulta (PostgreSQL) ---")
            conn = db_postgres.conectar()
            if conn:
                db_postgres.listar_clientes(conn)
                conn.close()
            else:
                print("(Não foi possível listar clientes do Postgres)")
            # -------------------------------------------------

            cpf = input("Digite o CPF para buscar no Cache: ")
            
            dados = buscar_recomendacao(cpf)
            if dados:
                print(f"\n✅ RECOMENDAÇÃO ENCONTRADA (CACHE):")
                print(json.dumps(dados, indent=4, ensure_ascii=False))
            else:
                print("⚠️ Nenhuma recomendação cacheada para este CPF.")
                print("   -> Dica: Vá na opção '6. GERAR RECOMENDAÇÕES' do menu principal primeiro.")
                
        elif op == '2':
            limpar_cache()
        elif op == '0':
            break

if __name__ == "__main__":
    if testar_conexao_redis():
        menu_redis()
    else:
        print("❌ Redis não encontrado.")