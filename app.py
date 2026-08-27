from flask import Flask, render_template, request
import os
import psycopg


app = Flask(__name__)


# ============================================================
# NORMALIZAÇÃO DA PESQUISA
# ============================================================

def normalizar_texto(texto):

    texto = texto.upper()

    texto = texto.replace("_", " ")
    texto = texto.replace("-", " ")

    palavras = texto.split()

    palavras_ignoradas = {
        "LEATHER",
        "LEATH"
    }

    palavras = [
        palavra
        for palavra in palavras
        if palavra not in palavras_ignoradas
    ]

    return palavras


# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

def conectar_banco():

    return psycopg.connect(
        os.environ["DATABASE_URL"]
    )


# ============================================================
# CRIAÇÃO DA TABELA
# ============================================================

def criar_banco():

    conexao = conectar_banco()

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
    conexao.close()


criar_banco()


# ============================================================
# PÁGINA INICIAL
# ============================================================

@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )


# ============================================================
# CONSULTA DE ESTOQUE
# ============================================================

@app.route("/consulta")
def consulta():

    modelo_pesquisado = request.args.get(
        "modelo",
        ""
    )

    conexao = conectar_banco()


    # --------------------------------------------------------
    # BUSCA DOS PRODUTOS
    # --------------------------------------------------------

    if modelo_pesquisado:

        todos_produtos = conexao.execute(
            """
            SELECT modelo, tamanho
            FROM estoque
            ORDER BY modelo, tamanho
            """
        ).fetchall()

        pesquisa_normalizada = normalizar_texto(
            modelo_pesquisado
        )

        produtos = []

        for produto in todos_produtos:

            modelo_banco = produto[0]

            modelo_normalizado = normalizar_texto(
                modelo_banco
            )

            if all(
                palavra in modelo_normalizado
                for palavra in pesquisa_normalizada
            ):
                produtos.append(
                    produto
                )

    else:

        produtos = []


    conexao.close()


    # --------------------------------------------------------
    # AGRUPAMENTO DOS TAMANHOS POR MODELO
    # --------------------------------------------------------

    produtos_agrupados = {}

    for produto in produtos:

        modelo = produto[0]
        tamanho = produto[1]

        if modelo not in produtos_agrupados:

            produtos_agrupados[modelo] = []

        produtos_agrupados[modelo].append(
            tamanho
        )


    # --------------------------------------------------------
    # CÁLCULO DAS GRADES
    # --------------------------------------------------------

    grades = {}

    for modelo, tamanhos in produtos_agrupados.items():

        lista_tamanhos = sorted(
            set(tamanhos)
        )

        menor_tamanho = min(
            lista_tamanhos
        )

        maior_tamanho = max(
            lista_tamanhos
        )

        nome_modelo = modelo.upper()


        # ----------------------------------------------------
        # BABY
        # ----------------------------------------------------

        if "BABY" in nome_modelo:

            grade_esperada = [
                15,
                17
            ]


        # ----------------------------------------------------
        # SMALL
        # ----------------------------------------------------

        elif "SMALL" in nome_modelo:

            grade_esperada = list(
                range(
                    menor_tamanho,
                    maior_tamanho + 1
                )
            )


        # ----------------------------------------------------
        # ACESSÓRIOS
        # ----------------------------------------------------

        elif (
            "LACES" in nome_modelo
            or "TOTE" in nome_modelo
        ):

            grade_esperada = (
                lista_tamanhos
            )


        # ----------------------------------------------------
        # MODELOS NORMAIS
        # ----------------------------------------------------

        else:

            grade_esperada = list(
                range(
                    menor_tamanho,
                    maior_tamanho + 1
                )
            )


        # ----------------------------------------------------
        # TAMANHOS QUE NÃO CONSTAM
        # ----------------------------------------------------

        tamanhos_faltantes = [
            tamanho
            for tamanho in grade_esperada
            if tamanho not in lista_tamanhos
        ]


        grades[modelo] = {

            "menor": menor_tamanho,

            "maior": maior_tamanho,

            "faltantes": tamanhos_faltantes
        }


    return render_template(
        "consulta.html",
        produtos_agrupados=produtos_agrupados,
        grades=grades,
        modelo_pesquisado=modelo_pesquisado
    )


# ============================================================
# MOVIMENTAÇÃO DE ESTOQUE
# ============================================================

@app.route(
    "/movimentar",
    methods=["POST"]
)
def movimentar():

    modelo = request.form["modelo"]

    tamanho = int(
        request.form["tamanho"]
    )

    movimentacao = request.form[
        "movimentacao"
    ]

    quantidade = int(
        request.form["quantidade"]
    )

    mensagem = ""

    conexao = conectar_banco()


    # --------------------------------------------------------
    # ENTRADA
    # --------------------------------------------------------

    if movimentacao == "Entrada":

        produto = conexao.execute(
            """
            SELECT *
            FROM estoque
            WHERE modelo = %s
            AND tamanho = %s
            """,
            (
                modelo,
                tamanho
            )
        ).fetchone()


        if produto:

            conexao.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade + %s
                WHERE modelo = %s
                AND tamanho = %s
                """,
                (
                    quantidade,
                    modelo,
                    tamanho
                )
            )

        else:

            conexao.execute(
                """
                INSERT INTO estoque (
                    modelo,
                    tamanho,
                    quantidade
                )
                VALUES (%s, %s, %s)
                """,
                (
                    modelo,
                    tamanho,
                    quantidade
                )
            )


        conexao.commit()

        mensagem = (
            "Entrada realizada!"
        )


    # --------------------------------------------------------
    # SAÍDA
    # --------------------------------------------------------

    elif movimentacao == "Saída":

        produto = conexao.execute(
            """
            SELECT *
            FROM estoque
            WHERE modelo = %s
            AND tamanho = %s
            """,
            (
                modelo,
                tamanho
            )
        ).fetchone()


        if produto is None:

            mensagem = (
                "Produto não encontrado no estoque!"
            )


        elif produto[3] < quantidade:

            mensagem = (
                "Estoque insuficiente!"
            )


        else:

            conexao.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade - %s
                WHERE modelo = %s
                AND tamanho = %s
                """,
                (
                    quantidade,
                    modelo,
                    tamanho
                )
            )

            conexao.commit()

            mensagem = (
                "Saída realizada!"
            )


    conexao.close()


    return f"""
    Modelo: {modelo}<br>
    Tamanho: {tamanho}<br>
    Movimentação: {movimentacao}<br>
    Quantidade: {quantidade}<br><br>

    {mensagem}
    """


# ============================================================
# VISUALIZAÇÃO TÉCNICA DO BANCO
# ============================================================

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