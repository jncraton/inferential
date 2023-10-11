from flask import *
import requests
from flask_restful import Api, Resource
import replicate
import os
app = Flask(__name__)
api = Api(app)
url = "http://127.0.0.1:5000/"
#Backend
class Test(Resource):
    def post(self):
        return {"data" : "Hello from the post method"}
    
class LLM(Resource):
    def get(self, chat):
        return {"data" : f"{chat}"}
    def post(self, chat):
         
        os.environ["REPLICATE_API_TOKEN"] = "r8_LXTUgUTjQpqTTqpDk1fLR7ZBvSW8pej0EKweF"

        pre_prompt = "You are an assistant. You do not respond as a 'User' or pretend to be a 'User'. You only respon once as 'Assistant'."
        prompt_input = str(chat)

        # Generate LLM response
        # This is a combo of the llm, input prompt for the model and the users input, and its range of error
        output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                        input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ", # Prompts
                        "temperature":0.75, "top_p":0.9, "max_length":200, "repetition_penalty":1})                
        reply = ""
        for item in output:
            reply+=item
        return {"data" : f"{reply}"}

api.add_resource(Test, "/test") 
api.add_resource(LLM, "/LLM/<string:chat>")

#Front end
@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        # For now, the output is just the input
        output = request.form["input"]
        chat = {"user_chat": output}
        #response = requests.post(url + "LLM/?chat=" + chat)
        requests.post(url + "LLM" , json=chat)
        return render_template("index.html",output=output, outputDisplay="block")
    else:
        return render_template("index.html", output="", outputDisplay="none")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )
