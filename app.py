""" This Flask application serves as the backend for the "Inferential" web app. It includes routes for accessing model status, rendering the loading page, providing the API endpoint for model inference, and serving the main playground page.

Configuration and Model Loading:
    - Reads configuration from 'config.yml' to set up model information and logos.
"""

import yaml
import sqlite3
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
    return render_template(
        "playground.html", models=config["models"], logo=config["logo"]
    )


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
    if len(query) >= models[model_name]["max_prompt_length"]:
        return (
            f"Error: The prompt exceeded maximum length of {models[model_name]['max_prompt_length']} .",
            413,
        )  # 413 Content Too Large
    if not "model" in models[model_name]:
        return (
            f"Error: Model '{model_name}' is not yet loaded.",
            503,
        )  # 503 Service Unavailable

    return Response(generate(query, model_name), content_type="text/plain")


@app.route("/api/status")
def api_status_page():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select model, sum(1) as count from requests")

    reqs = {m["model"]: m["count"] for m in cursor.fetchall()}

    status = [
        {"name": m["name"], "loaded": "model" in m, "requests": reqs.get(m["name"], 0)}
        for m in models.values()
    ]

    return {"models": status, "loadedAll": all(m["loaded"] for m in status)}
