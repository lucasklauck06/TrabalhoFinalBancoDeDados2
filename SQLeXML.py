import psycopg2
import xml.etree.ElementTree as ET

# -------------------------
# 1) Conectar ao PostgreSQL
# -------------------------
conn = psycopg2.connect(
    host="localhost",
    database="seubanco",
    user="seuusuario",
    password="suasenha"
)
cur = conn.cursor()

# -------------------------
# 2) Buscar tabela Peca
# -------------------------
cur.execute("SELECT cod_peca, pnome, cor, peso, cdade FROM Peca;")
pecas_pg = cur.fetchall()

# Converte em dicionário para acesso rápido
pecas_dict = {
    str(l[0]): {   # chave: cod_peca (ex: "1")
        "cod_peca": l[0],
        "pnome": l[1],
        "cor": l[2],
        "peso": l[3],
        "cidade": l[4],
    }
    for l in pecas_pg
}

# -------------------------
# 3) Ler fornecimento.xml
# -------------------------
tree = ET.parse("fornecimento.xml")
root = tree.getroot()

fornecimentos = []

for f in root.findall("fornecimento"):
    cod_peca_xml = f.find("Cod_Peca").text   # ex: P1
    cod_peca_num = cod_peca_xml.replace("P", "")  # vira "1"

    fornecimentos.append({
        "cod_fornec": f.find("Cod_Fornec").text,
        "cod_peca": cod_peca_num,  # agora combina com PostgreSQL
        "cod_proj": f.find("Cod_Proj").text,
        "quantidade": f.find("Quantidade").text
    })

# -------------------------
# 4) Fazer a junção
# -------------------------

resultado = []

for f in fornecimentos:
    cod = f["cod_peca"]

    if cod in pecas_dict:
        resultado.append({
            "peca": pecas_dict[cod],
            "fornecimento": f
        })

# -------------------------
# 5) Exibir resultado
# -------------------------

for r in resultado:
    print("==== INTEGRAÇÃO ====")
    print("Peça (PostgreSQL):")
    print(r["peca"])
    print("Fornecimento (XML):")
    print(r["fornecimento"])
    print()
