from flask import Flask, request, jsonify
from unidecode import unidecode

app = Flask(__name__)

# Pasar parametros en la url --> @app.route("/ruta/<param>")
# parametros con su tipo --> @app.route("/ruta/<string:param>") --> string,int,float
@app.route("/")
def index():
    return "<p>Hello Flask!</p>"

@app.route("/api/translate", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        content = request.json
        #texto formateado, se quitan comillas, mayusculas, etc.
        formattedText = unidecode(content['mapudungun']).lower()
        print(formattedText)
        #se retorna un json con el texto formateado
        return jsonify({'formattedText':formattedText})

if __name__ == '__main__':
    app.run(debug=True)