import pandas as pd
import sqlite3


arquivo = "Sistema Estoque.xlsb"

df = pd.read_excel(
    arquivo,
    sheet_name="BASE DE DADOS SESSÃO",
    engine="pyxlsb"
)

df.columns = df.columns.str.strip()

df[["Modelo", "Tamanho"]] = df["Descrição Mercadoria"].str.rsplit(
    ",",
    n=1,
    expand=True
)

df["Modelo"] = df["Modelo"].str.strip()
df["Tamanho"] = df["Tamanho"].str.strip()
df["Tamanho"] = pd.to_numeric(df["Tamanho"], errors="coerce")
df["Físico"] = pd.to_numeric(df["Físico"], errors="coerce")

df = df[["Modelo", "Tamanho", "Físico"]].dropna(subset=["Modelo", "Tamanho", "Físico"])

df["Tamanho"] = df["Tamanho"].astype(int)
df["Físico"] = df["Físico"].astype(int)


print(df[["Modelo", "Tamanho", "Físico"]].head())
print(df[["Modelo", "Tamanho", "Físico"]].dtypes)


dados_estoque = df[["Modelo", "Tamanho", "Físico"]]
dados_estoque =(
        dados_estoque.groupby(["Modelo", "Tamanho"], as_index=False)["Físico"].sum()
    )

print(dados_estoque.head())
print(f"\nTotal de registros válidos: {len(dados_estoque)}")

duplicados = dados_estoque.duplicated(
    subset=["Modelo", "Tamanho"],
    keep=False
)


print("\nRegistros duplicados por Modelo + Tamanho:")
print(dados_estoque[duplicados])

print(f"\nTotal de linhas duplicadas: {duplicados.sum()}")

fisico_negativo = dados_estoque[dados_estoque["Físico"]<0]

tamanhos_suspeitos = dados_estoque[
    ~(
    dados_estoque["Tamanho"] .between(20, 50)
    |
    dados_estoque["Tamanho"].isin([15,17,19,115,125,135,145])
    )
]

print("\nRegistros com Físico negativo:")
print(fisico_negativo)

print("\nRegistros com tamanho suspeito:")
print(tamanhos_suspeitos)

print(f"\nTotal com Físico negativo: {len(fisico_negativo)}")
print(f"Total com tamanho suspeito: {len(tamanhos_suspeitos)}")


conexao = sqlite3.connect("estoque.db")

inseridos = 0
atualizados = 0

for _, produto in dados_estoque.iterrows():

    modelo = produto["Modelo"]
    tamanho = int(produto["Tamanho"])
    quantidade = int(produto["Físico"])

    produto_banco = conexao.execute(
        """
        SELECT * FROM estoque
        WHERE modelo = ? AND tamanho = ?
        """,
        (modelo, tamanho)
    ).fetchone()

    if produto_banco is None:
        conexao.execute(
            """
            INSERT INTO estoque (modelo, tamanho, quantidade)
            VALUES (?, ?, ?)
            """,
            (modelo, tamanho, quantidade)
        )

        inseridos += 1

    else:
        conexao.execute(
            """
            UPDATE estoque
            SET quantidade = ?
            WHERE modelo = ? AND tamanho = ?
            """,
            (quantidade, modelo, tamanho)
        )

        atualizados += 1

conexao.commit()
conexao.close()

print("\nSincronização concluída!")
print(f"Produtos inseridos: {inseridos}")
print(f"Produtos atualizados: {atualizados}")




