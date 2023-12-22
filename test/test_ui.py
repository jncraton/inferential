"""Test UI of web application. Requires running application."""

import pytest
from playwright.sync_api import Page, expect


def test_text_appears(page: Page):
    """This will test a basic query."""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()

    # Wait for the output to appear, adjust the selector accordingly
    chat_reply = page.wait_for_selector("#outputResponse")

    # Check if the generated text is not empty
    generated_text = chat_reply.inner_text()
    assert generated_text.strip() != "", "Generated text is empty"


def test_empty_query(page: Page):
    """This will test if the user queries an empty string"""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text("Error: No prompt was provided.")


def test_query_too_big(page: Page):
    """This will test if the query of a user is to big"""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").fill("a " * 10000)
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text(f"prompt exceeded maximum length")


def test_dropdown_input(page: Page):
    """This will test the dropdown inputs"""
    # Opens the config file and assigns it to config_index
    page.goto("http://127.0.0.1:5000/playground")
    dropdown = page.locator("select[id='modelSelect']")
    i = 0
    for model in pytest.conf["models"]:
        dropdown.select_option(index=i)
        expect(dropdown).to_contain_text(model["name"])
        i += 1


def test_shift_enter(page: Page):
    """This will test if shift+enter creates a new line"""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").press("Shift+Enter")
    expect(page.get_by_label("Prompt")).to_contain_text("\n")


def test_enter(page: Page):
    """This will test if enter submits prompt"""
    page.goto("http://127.0.0.1:5000/playground")
    prompt_box = page.get_by_label("Prompt")
    prompt_box.press("Enter")
    expect(prompt_box).to_contain_text("")
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text("Error: No prompt was provided.")


def test_redirect(page: Page):
    """This test makes sure the nav bar works by testing the first navigation link on the playground"""
    page.goto("http://127.0.0.1:5000/playground")
    page.query_selector("nav li:first-child a").click()
    assert page.url == "http://127.0.0.1:5000/status"


def test_logo_appears(page: Page):
    """This will test if the logo appears on the main playground page."""
    page.goto("http://127.0.0.1:5000/playground")
    nav_logo = page.locator("nav img")
    expect(nav_logo).to_be_visible()


def test_disable_api_during_request(page: Page):
    """This will test if the submit button is disabled during the API request."""
    page.goto("http://127.0.0.1:5000/playground")
    submit_button = page.get_by_role("button", name="Submit")
    page.get_by_label("Prompt").fill("Where is Paris")
    submit_button.click()
    expect(submit_button).to_be_disabled()
    page.wait_for_selector("#outputResponse:not(:empty)")
    expect(submit_button).not_to_be_disabled()


def test_loading_spinner(page: Page):
    """Test if the loading spinner is visible when a response is being generated."""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()
    loading_spinner = page.locator("#loadingSpinner")
    expect(loading_spinner).to_be_visible()
    page.wait_for_selector("#loadingSpinner", state="hidden")
    expect(loading_spinner).to_be_hidden()


def test_max_tokens(page: Page):
    """Verify that max_tokens field limits response size"""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").fill("What is the capital of France?")
    page.get_by_text("Generation parameters").click()
    page.get_by_label("Max tokens").fill("1")
    page.get_by_role("button", name="Submit").click()

    assert page.wait_for_selector("#outputResponse").inner_text() == "Paris"
