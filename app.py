from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route("/movimentar", methods=["POST"])
def movimentar():

    modelo = request.form["modelo"]
    tamanho = int(request.form["tamanho"])
    movimentacao = request.form["movimentacao"]
    quantidade = int(request.form["quantidade"])

    if movimentacao == "Entrada":
        mensagem = "Entrada realizada!"

    elif movimentacao == "Saída":
        mensagem = "Saída realizada!"

    return f"""
    Modelo: {modelo}<br>
    Tamanho: {tamanho}<br>
    Movimentação: {movimentacao}<br>
    Quantidade: {quantidade}<br><br>

    {mensagem}
    """