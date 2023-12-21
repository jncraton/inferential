""" This module contains test cases using Pytest and Playwright for the "Inferential" web app.
 The tests cover various aspects including API responses, user interactions, form validations, navigation, and visual elements."""

import yaml
import pytest
from playwright.sync_api import Page, expect


def test_text_appears(page: Page):
    """This will test a basic query."""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").click()
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
    with open("config.yml", "r") as f:
        config_models = yaml.safe_load(f)["models"]
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").click()
    page.get_by_label("Prompt").fill("a " * config_models[0]["max_prompt_length"])
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text(
        f"Error: The prompt exceeded maximum length of {config_models[0]['max_prompt_length']} ."
    )


def test_dropdown_input(page: Page):
    """This will test the dropdown inputs"""
    # Opens the config file and assigns it to config_index
    with open("config.yml", "r") as f:
        config_models = yaml.safe_load(f)["models"]
    page.goto("http://127.0.0.1:5000/playground")
    dropdown = page.locator("select[id='modelSelect']")
    i = 0
    for model in config_models:
        dropdown.select_option(index=i)
        expect(dropdown).to_contain_text(model["name"])
        i += 1


def test_shift_enter(page: Page):
    """This will test if shift+enter creates a new line"""
    page.goto("http://127.0.0.1:5000/playground")
    prompt_box = page.get_by_label("Prompt")
    prompt_box.click()
    prompt_box.press("Shift+Enter")
    expect(prompt_box).to_contain_text("\n")


def test_enter(page: Page):
    """This will test if enter submits prompt"""
    page.goto("http://127.0.0.1:5000/playground")
    prompt_box = page.get_by_label("Prompt")
    prompt_box.click()
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
    nav_logo = page.locator("nav .body_logo")
    expect(nav_logo).to_be_visible()
    body_logo = page.locator(".body_logo")
    expect(body_logo).to_be_visible()


def test_disable_api_during_request(page: Page):
    """This will test if the submit button is disabled during the API request."""
    page.goto("http://127.0.0.1:5000/playground")
    prompt_box = page.get_by_label("Prompt")
    submit_button = page.get_by_role("button", name="Submit")
    prompt_box.click()
    prompt_box.fill("Where is Paris")
    submit_button.click()
    expect(submit_button).to_be_disabled()
    page.wait_for_selector("#outputResponse:not(:empty)")
    expect(submit_button).not_to_be_disabled()


def test_loading_spinner(page: Page):
    """Test if the loading spinner is visible when a response is being generated."""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").click()
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()
    loading_spinner = page.locator("#loadingSpinner")
    expect(loading_spinner).to_be_visible()
    page.wait_for_selector("#loadingSpinner", state="hidden")
    expect(loading_spinner).to_be_hidden()
