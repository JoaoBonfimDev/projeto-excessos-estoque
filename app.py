from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
def criar_banco():
    conexao = sqlite3.connect("estoque.db")

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            tamanho INTEGER NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)

    conexao.close()

criar_banco()
@app.route('/')
def inicio():
    return render_template('index.html')
@app.route("/consulta")
def consulta():
    return render_template("consulta.html")

@app.route("/movimentar", methods=["POST"])
def movimentar():
    modelo = request.form["modelo"]
    tamanho = int(request.form["tamanho"])
    movimentacao = request.form["movimentacao"]
    quantidade = int(request.form["quantidade"])
    mensagem = ""

    if movimentacao == "Entrada":

        conexao = sqlite3.connect("estoque.db")

        produto = conexao.execute(
            """

            SELECT * FROM estoque 
            WHERE modelo = ? AND tamanho = ?
            """,
            (modelo, tamanho)
        ).fetchone()

        if produto:
            conexao.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade + ?
                WHERE modelo = ? AND tamanho = ?
                """,
                (quantidade, modelo, tamanho)
            )
        else:
            conexao.execute(
                """
                INSERT INTO estoque (modelo, tamanho, quantidade)
                VALUES (?, ?, ?)
                """,
                (modelo, tamanho, quantidade)
            )

        conexao.commit()
        conexao.close()
        mensagem = "Entrada realizada!"


    elif movimentacao == "Saída":

        conexao = sqlite3.connect("estoque.db")

        produto = conexao.execute(
            """
            SELECT * FROM estoque
            WHERE modelo = ? AND tamanho = ?
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
                SET quantidade = quantidade - ?
                WHERE modelo = ? AND tamanho = ?
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

    conexao = sqlite3.connect("estoque.db")

    produtos = conexao.execute(
        "SELECT * FROM estoque"
    ).fetchall()

    conexao.close()

    return str(produtos)