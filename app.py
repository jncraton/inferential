import yaml
from flask import Flask, Response, request, render_template, send_from_directory
from inference import generate, models, config

app = Flask(__name__)


# Landing page
@app.route("/")
def landing_page():
    return render_template("landing.html", logo=config["logo"])


# Loading page
@app.route("/status")
def loading_page():
    return render_template("status.html", logo=config["logo"])


# API Front End
@app.route("/playground")
def playground():
    return render_template("index.html", models=config["models"], logo=config["logo"])


# Backend
@app.route("/api")
def api():
    query = request.args.get("input", "")
    model_name = request.args.get("model", config["models"][0]["name"])

    if query == "":
        return "Error: No prompt was provided.", 400  # 400 Bad Request
    if not model_name in models:
        # 400 Bad Request
        return f"Error: Unknown model name '{model_name}'.", 400
    if len(query) >= models[model_name]["maxPromptLength"]:
        return "Error: The prompt was too long.", 413  # 413 Content Too Large
    if not "model" in models[model_name]:
        return (
            f"Error: Model '{model_name}' is not yet loaded.",
            503,
        )  # 503 Service Unavailable

    return Response(generate(query, model_name), content_type="text/plain")


@app.route("/api/status")
def api_status_page():
    status = [{"name": m["name"], "loaded": "model" in m} for m in models.values()]

    return {"models": status, "loadedAll": all(m["loaded"] for m in status)}
