"""Tests for the /api endpoints"""

import pytest


def test_model_download_api(client):
    """Verify the status endpoint returns an appropriate object"""
    response = client.get("/api/status")
    assert response.status_code == 200
    assert len(response.json["models"]) == 3


def test_paris_query_api(client):
    """This will test to verify a status for a normal query"""
    response = client.get("/api?input=What is the capital of France?")
    assert response.status_code == 200
    assert response.text == "Paris."


def test_status_req_count(client):
    """Verify that request count increase in the status endpoint"""
    response = client.get("/api/status")
    previous = response.json["models"][0]["requests"]

    response = client.get("/api?input=What is the capital of France?")
    assert response.text == "Paris."

    response = client.get("/api/status")
    assert response.json["models"][0]["requests"] == previous + 1


def test_empty_query_api(client):
    """This will test to verify a status for empty query"""
    response = client.get("/api?input=")
    assert response.status_code == 400


def test_query_too_big_api(client):
    """This will test verify status code for a too big query"""
    for model in pytest.conf["models"]:
        response = client.get(f"/api?input={'a ' * 10000}")
        assert response.status_code == 413


def test_invalid_model_name_api(client):
    """This will test to verify the status code and response text for an invalid model name in an API request"""
    response = client.get("/api?input=Hello&model=example-invalid-model-name")
    assert response.text == "Error: Unknown model name 'example-invalid-model-name'."
    assert response.status_code == 400


def test_all_models_name_api(client):
    """This will test to verify all models in config file return valid status code"""
    for model in pytest.conf["models"]:
        response = client.get("/api?input=Where is Paris&model=" + model["name"])
        assert response.status_code == 200


def test_streaming(client):
    """This test will confirm that the response is streamed"""
    response = client.get("/api?input=hielo")
    assert response.is_streamed == True
