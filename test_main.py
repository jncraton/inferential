import pytest
from app import *
from playwright.sync_api import *


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_placeholder():
    assert True


def test_paris(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_label("Prompt").click()
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()
    output_value = page.locator(".output").inner_text()
    assert "France" in output_value


def test_empty_chat(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("button", name="Submit").click()
    output_value = page.locator(".output").inner_text()
    assert "Enter a valid input!" in output_value


def test_chat_too_big(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_label("Prompt").click()
    chat_input = page.locator(".input").inner_text()
    page.get_by_role("button", name="Submit").click()
    output_value = page.locator(".output").inner_text()
    assert ("Enter a valid input!" in output_value) and len(str(chat_input)) >= 500
