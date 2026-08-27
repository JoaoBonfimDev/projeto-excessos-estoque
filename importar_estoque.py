import pandas as pd
import psycopg
import os


# ============================================================
# 1. LEITURA DA PLANILHA
# ============================================================

arquivo = "Sistema Estoque.xlsb"

df = pd.read_excel(
    arquivo,
    sheet_name="BASE DE DADOS SESSÃO",
    engine="pyxlsb"
)


# ============================================================
# 2. TRATAMENTO DAS COLUNAS
# ============================================================

df.columns = df.columns.str.strip()

df[["Modelo", "Tamanho"]] = df["Descrição Mercadoria"].str.rsplit(
    ",",
    n=1,
    expand=True
)

df["Modelo"] = df["Modelo"].str.strip()

df["Tamanho"] = df["Tamanho"].str.strip()
df["Tamanho"] = pd.to_numeric(
    df["Tamanho"],
    errors="coerce"
)

df["Físico"] = pd.to_numeric(
    df["Físico"],
    errors="coerce"
)

df = df[
    ["Modelo", "Tamanho", "Físico"]
].dropna(
    subset=["Modelo", "Tamanho", "Físico"]
)

df["Tamanho"] = df["Tamanho"].astype(int)
df["Físico"] = df["Físico"].astype(int)


# ============================================================
# 3. CONFERÊNCIA DOS DADOS
# ============================================================

print(df[["Modelo", "Tamanho", "Físico"]].head())

print(
    df[["Modelo", "Tamanho", "Físico"]].dtypes
)


# ============================================================
# 4. AGRUPAMENTO DO ESTOQUE
# ============================================================

dados_estoque = df[
    ["Modelo", "Tamanho", "Físico"]
]

dados_estoque = (
    dados_estoque
    .groupby(
        ["Modelo", "Tamanho"],
        as_index=False
    )["Físico"]
    .sum()
)

print(dados_estoque.head())

print(
    f"\nTotal de registros válidos: "
    f"{len(dados_estoque)}"
)


# ============================================================
# 5. VERIFICAÇÃO DE DUPLICADOS
# ============================================================

duplicados = dados_estoque.duplicated(
    subset=["Modelo", "Tamanho"],
    keep=False
)

print(
    "\nRegistros duplicados "
    "por Modelo + Tamanho:"
)

print(
    dados_estoque[duplicados]
)

print(
    f"\nTotal de linhas duplicadas: "
    f"{duplicados.sum()}"
)


# ============================================================
# 6. VALIDAÇÕES
# ============================================================

fisico_negativo = dados_estoque[
    dados_estoque["Físico"] < 0
]

tamanhos_suspeitos = dados_estoque[
    ~(
        dados_estoque["Tamanho"].between(20, 50)
        |
        dados_estoque["Tamanho"].isin(
            [15, 17, 19, 115, 125, 135, 145]
        )
    )
]

print("\nRegistros com Físico negativo:")
print(fisico_negativo)

print("\nRegistros com tamanho suspeito:")
print(tamanhos_suspeitos)

print(
    f"\nTotal com Físico negativo: "
    f"{len(fisico_negativo)}"
)

print(
    f"Total com tamanho suspeito: "
    f"{len(tamanhos_suspeitos)}"
)


# ============================================================
# 7. CONEXÃO COM POSTGRESQL
# ============================================================

print("\nConectando ao PostgreSQL...")

conexao = psycopg.connect(
    os.environ["DATABASE_URL"]
)

print("Conexão realizada com sucesso!")


# ============================================================
# 8. CRIAÇÃO DA TABELA
# ============================================================

conexao.execute(
    """
    CREATE TABLE IF NOT EXISTS estoque (
        id SERIAL PRIMARY KEY,
        modelo TEXT NOT NULL,
        tamanho INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        UNIQUE (modelo, tamanho)
    )
    """
)

conexao.commit()


# ============================================================
# 9. GARANTE UNIQUE PARA TABELA JÁ EXISTENTE
# ============================================================

conexao.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS
    estoque_modelo_tamanho_unique
    ON estoque (modelo, tamanho)
    """
)

conexao.commit()


# ============================================================
# 10. PREPARAÇÃO DOS DADOS PARA O POSTGRESQL
# ============================================================

produtos = []

for _, produto in dados_estoque.iterrows():

    produtos.append(
        (
            produto["Modelo"],
            int(produto["Tamanho"]),
            int(produto["Físico"])
        )
    )


# ============================================================
# 11. SINCRONIZAÇÃO COM UPSERT
# ============================================================

print(
    f"\nSincronizando "
    f"{len(produtos)} produtos..."
)

with conexao.cursor() as cursor:

    cursor.executemany(
        """
        INSERT INTO estoque (
            modelo,
            tamanho,
            quantidade
        )
        VALUES (%s, %s, %s)

        ON CONFLICT (modelo, tamanho)

        DO UPDATE SET
            quantidade = EXCLUDED.quantidade
        """,
        produtos
    )


conexao.commit()


# ============================================================
# 12. CONFERÊNCIA FINAL
# ============================================================

total_banco = conexao.execute(
    """
    SELECT COUNT(*)
    FROM estoque
    """
).fetchone()[0]

conexao.close()


print("\nSincronização concluída!")

print(
    f"Produtos processados: "
    f"{len(produtos)}"
)

print(
    f"Total de registros no banco: "
    f"{total_banco}"
)