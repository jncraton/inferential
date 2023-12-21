import pytest
from inferential.stats import log, get_model_stats


def test_log(client):
    """Verity database insertion when logging"""
    start_reqs = get_model_stats()["models"][-1]["requests"]

    log("marella/gpt-2-ggml", 1, 2)
    end_reqs = get_model_stats()["models"][-1]["requests"]
    assert end_reqs == start_reqs + 1
