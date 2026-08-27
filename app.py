from flask import Flask, render_template, request
import os
import psycopg


app = Flask(__name__)


def conectar_banco():
    return psycopg.connect(os.environ["DATABASE_URL"])


def criar_banco():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id SERIAL PRIMARY KEY,
            modelo TEXT NOT NULL,
            tamanho INTEGER NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


criar_banco()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/consulta")
def consulta():

    modelo_pesquisado = request.args.get("modelo", "")

    conexao = conectar_banco()

    if modelo_pesquisado:
        produtos = conexao.execute(
            """
            SELECT modelo, tamanho, quantidade
            FROM estoque
            WHERE modelo ILIKE %s
            ORDER BY modelo, tamanho
            """,
            (f"%{modelo_pesquisado}%",)
        ).fetchall()

    else:
        produtos = []

    produtos_agrupados = {}

    for produto in produtos:

        modelo = produto[0]
        tamanho = produto[1]
        quantidade = produto[2]

        if modelo not in produtos_agrupados:
            produtos_agrupados[modelo] = []

        produtos_agrupados[modelo].append(
            (tamanho, quantidade)
        )

    conexao.close()

    return render_template(
        "consulta.html",
        produtos=produtos,
        produtos_agrupados=produtos_agrupados,
        modelo_pesquisado=modelo_pesquisado
    )


@app.route("/movimentar", methods=["POST"])
def movimentar():

    modelo = request.form["modelo"]
    tamanho = int(request.form["tamanho"])
    movimentacao = request.form["movimentacao"]
    quantidade = int(request.form["quantidade"])

    mensagem = ""

    conexao = conectar_banco()

    if movimentacao == "Entrada":

        produto = conexao.execute(
            """
            SELECT * FROM estoque
            WHERE modelo = %s AND tamanho = %s
            """,
            (modelo, tamanho)
        ).fetchone()

        if produto:

            conexao.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade + %s
                WHERE modelo = %s AND tamanho = %s
                """,
                (quantidade, modelo, tamanho)
            )

        else:

            conexao.execute(
                """
                INSERT INTO estoque (modelo, tamanho, quantidade)
                VALUES (%s, %s, %s)
                """,
                (modelo, tamanho, quantidade)
            )

        conexao.commit()

        mensagem = "Entrada realizada!"


    elif movimentacao == "Saída":

        produto = conexao.execute(
            """
            SELECT * FROM estoque
            WHERE modelo = %s AND tamanho = %s
            """,
            (modelo, tamanho)
        ).fetchone()

        if produto is None:

            mensagem = "Produto não encontrado no estoque!"

        elif produto[3] < quantidade:

            mensagem = "Estoque insuficiente!"

        else:

            conexao.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade - %s
                WHERE modelo = %s AND tamanho = %s
                """,
                (quantidade, modelo, tamanho)
            )

            conexao.commit()

            mensagem = "Saída realizada!"

    conexao.close()

    return f"""
    Modelo: {modelo}<br>
    Tamanho: {tamanho}<br>
    Movimentação: {movimentacao}<br>
    Quantidade: {quantidade}<br><br>

    {mensagem}
    """


@app.route("/estoque")
def ver_estoque():

    conexao = conectar_banco()

    produtos = conexao.execute(
        """
        SELECT *
        FROM estoque
        ORDER BY modelo, tamanho
        """
    ).fetchall()

    conexao.close()

    return str(produtos)