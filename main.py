from flask import Flask,request
from unidecode import unidecode

app = Flask(__name__)

# Pasar parametros en la url --> @app.route("/ruta/<param>")
# parametros con su tipo --> @app.route("/ruta/<string:param>") --> string,int,float
@app.route("/")
def index():
    return "<p>Hello Flask!</p>"

@app.route("/about")
def about():
    return "<h1>about</h1>"

@app.route("/translate")
@app.route("/translate/<string:texto>")
def translate(texto = None):
    textoAux = ''
    #en request.method se obtiene el tipo de metodo (GET,POST,PUT)
    if texto != None:
        textoAux  = unidecode(texto).lower()
    return f"""
        <p>texto formateado: {textoAux}</p>
    """

if __name__ == '__main__':
    app.run(debug=True)