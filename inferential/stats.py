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


def populate():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    with open("schema.sql", "r") as file:
        sql = file.read()

    cursor.executescript(sql)
    conn.commit()
    conn.close()


def build_hour_stats(key, model, stats):
    sparse = {s["minutes_ago"]: s[key] for s in stats if s["model"] == model}

    return [sparse.get(i, 0) for i in range(60)]


def get_model_stats():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        select
          model,
          strftime('%s', 'now')/60 - time/60 as minutes_ago,
          sum(input_tokens) + sum(output_tokens) as tokens,
          sum(1) as requests
        from requests where time >= (strftime('%s', 'now') - 3600)
        group by model, time/60;
        """
    )

    stats = list(cursor.fetchall())

    status = [
        {
            "name": m["name"],
            "loaded": "model" in m,
            "requests_per_min": build_hour_stats("requests", m["name"], stats),
            "tokens_per_min": build_hour_stats("tokens", m["name"], stats),
        }
        for m in config["models"]
    ]

    return {"models": status, "loadedAll": all(m["loaded"] for m in status)}
