import pytest
from app import *
from playwright.sync_api import *
from random import choice
from string import ascii_lowercase


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_paris_query_api(client):
    response = client.get("/api?input=Where is Paris")
    assert response.status_code == 200


def test_paris_query(page: Page):
    """This will tests a basic query"""
    page.goto("http://127.0.0.1:5000/")
    page.get_by_label("Prompt").click()
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator(".output")
    expect(chat_reply).to_contain_text("France")


def test_empty_query(page: Page):
    """This will test if the user queries an empty string"""
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator(".output")
    expect(chat_reply).to_contain_text("Error: No prompt was provided.")


def test_empty_query_api(client):
    response = client.get("/api?input=")
    assert response.status_code == 400


def test_query_too_big(page: Page):
    """This will test if the query of a user is to big"""
    n = 250
    page.goto("http://127.0.0.1:5000/")
    page.get_by_label("Prompt").click()
    query = "a".join(choice(ascii_lowercase) for i in range(n))
    page.get_by_label("Prompt").fill(query)
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator(".output")
    expect(chat_reply).to_contain_text("Error: The prompt was too long.")


def test_query_too_big_api(client):
    response = client.get(
        "/api?input=" + ("".join(choice(ascii_lowercase) for i in range(250)))
    )
    assert response.status_code == 413
