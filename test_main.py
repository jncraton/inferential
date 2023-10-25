import pytest
from app import *
from playwright.sync_api import *
from random import choice
from string import ascii_lowercase

@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()

#Tests the LLM model is smart enough to say Paris is in France
def test_paris_query(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_label("Prompt").click()
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()
    output_value = page.locator(".output").inner_text()
    assert "France" in output_value

#Tests for correct response when prompted with an empty query
def test_empty_query(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("button", name="Submit").click()
    output_value = page.locator(".output").inner_text()
    assert "Enter a valid query!" in output_value

#Tests for the correct response when given a query too big
def test_query_too_big(page: Page):
    n = 250
    page.goto("http://127.0.0.1:5000/")
    page.get_by_label("Prompt").click()
    query = "a".join(choice(ascii_lowercase) for i in range(n))
    page.get_by_label("Prompt").fill(query)
    page.get_by_role("button", name="Submit").click()
    output_value = page.locator(".output").inner_text()
    assert "Enter a valid query!" in output_value