import pytest
from inferential.config import config


def test_logo():
    """Verify log field is present and read properly"""
    assert config["logo"].endswith(".png")


def test_model_list():
    """Verify that a model list is loaded"""
    assert len(config["models"]) > 1
