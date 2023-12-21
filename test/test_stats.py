import pytest
from inferential.stats import log, get_model_stats


def test_log(client):
    """Verity database insertion when logging"""
    start_reqs = get_model_stats().get("test_log", 0)

    log("test_log", 1, 2)
    end_reqs = get_model_stats().get("test_log", 0)
    assert end_reqs == start_reqs + 1
