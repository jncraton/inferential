from flask import *
import requests
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)
url = "http://127.0.0.1:5000/"
#Backend
class Test(Resource):
    def get(self):
        return {"data" : "Get"}
    def post(self,chat):
        self.chat = chat
        return {"data" : self.chat}
    def llm(self):
        return "Text"
api.add_resource(Test, "/") 


#Front end
@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        # For now, the output is just the input
        output = request.form["input"]
        chat = {"chat" : output}
        Test.post(chat)
        return  render_template("index.html", outputDisplay="block")
    else:
        return render_template("index.html", output="", outputDisplay="none")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )
