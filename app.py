from flask import *
import languagemodels as lm
from markupsafe import escape
import requests
import psutil

app = Flask(__name__)


# Front end
@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        # For now, the output is just the input
        output = escape(request.form["input"])
        api_route = requests.get("http://127.0.0.1:5000/api?output= " + f"{output}")
        response = api_route.json()
        return render_template(
            "index.html", output=response["data"], outputDisplay="block"
        )
    else:
        return render_template("index.html", output="", outputDisplay="none")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


# Backend


@app.route("/api")
def api():
    chat = request.args.get("output", "")

    # changes ram the llm is using dynamic to half of avaiable ram to imporve accuracy
    freeRam = psutil.virtual_memory().free
    lm.set_max_ram(freeRam / 2)

    reply = lm.do(chat)
    data = {"data" : reply}
    return data,200 #returns the dictionary and a 200 response code 
