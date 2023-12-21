import sqlite3
from inferential.config import config


def log(model, input_toks, output_toks):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        "insert into requests(model, input_tokens, output_tokens) values (?,?,?)",
        (model, input_toks, output_toks),
    )
    conn.commit()


def get_model_stats():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select model, sum(1) as count from requests group by model")

    reqs = {m["model"]: m["count"] for m in cursor.fetchall()}

    status = [
        {
            "name": m["name"],
            "loaded": "model" in m,
            "requests": reqs.get(m["name"], 0),
        }
        for m in config["models"]
    ]

    return {"models": status, "loadedAll": all(m["loaded"] for m in status)}
