from flask import Flask, request, jsonify
from unidecode import unidecode
from traductor import translate

# para instalar dependecias y librerías empleadas (vease requeriments.txt)
# utilizar el comando: pip3 install -r requirements.txt

app = Flask(__name__)

#UTF-8
app.config['JSON_AS_ASCII'] = False


# Pasar parametros en la url --> @app.route("/ruta/<param>")
# parametros con su tipo --> @app.route("/ruta/<string:param>") --> string,int,float


@app.route("/")
def index():
    return "<p>Hello Flask!</p>"


@app.route("/api/traductor", methods=["POST"])
def traductor():
    # para mandar la petición (POST) mandar el json con el formato:
    # {"spanish":"texto en español"}
    if request.method == "POST":
        content = request.json
        # texto formateado, se quitan comillas, mayusculas, etc.
        formattedText = unidecode(content['spanish']).lower()
        # print(formattedText)
        translateToMapudungun = translate(formattedText)
        print(f"traduccion: {translateToMapudungun}")
        # se retorna un json con el texto formateado
        return jsonify({'mapudungun': translateToMapudungun})


if __name__ == '__main__':
    app.run(debug=True)
