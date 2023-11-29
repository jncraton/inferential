import pytest
from app import yaml, app
from playwright.sync_api import Page, expect
from random import choice
from string import ascii_lowercase
import time


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_model_download_api(client):
    """This test will confirm all of the models are ready"""
    response = client.get("/api/status")
    print(response.json)
    while not response.json["loadedAll"]:
        time.sleep(5)  # Waits 5 seconds
        response = client.get("/api/status")
    assert response.json["loadedAll"]


def test_paris_query_api(client):
    """This will test to verify a status for a normal query"""
    response = client.get("/api?input=Where is Paris")
    assert response.status_code == 200


def test_text_appears(page: Page):
    """This will test a basic query."""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").click()
    page.get_by_label("Prompt").fill("Where is Paris")
    page.get_by_role("button", name="Submit").click()

    # Wait for the output to appear, adjust the selector accordingly
    chat_reply = page.locator("#outputResponse")

    # Check if the generated text is not empty
    generated_text = chat_reply.inner_text()
    assert generated_text.strip() != "", "Generated text is empty"


def test_empty_query(page: Page):
    """This will test if the user queries an empty string"""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text("Error: No prompt was provided.")


def test_empty_query_api(client):
    """This will test to verify a status for empty query"""
    response = client.get("/api?input=")
    assert response.status_code == 400


def test_query_too_big(page: Page):
    """This will test if the query of a user is to big"""
    n = 250
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_label("Prompt").click()
    query = "a".join(choice(ascii_lowercase) for i in range(n))
    page.get_by_label("Prompt").fill(query)
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text("Error: The prompt was too long.")


def test_query_too_big_api(client):
    """This will test verify status code for a too big query"""
    response = client.get(
        "/api?input=" + ("".join(choice(ascii_lowercase) for i in range(250)))
    )
    assert response.status_code == 413


def test_invalid_model_name_api(client):
    """This will test to verify the status code and response text for an invalid model name in an API request"""
    response = client.get("/api?input=Hello&model=example-invalid-model-name")
    assert response.text == "Error: Unknown model name 'example-invalid-model-name'."
    assert response.status_code == 400


def test_all_models_name_api(client):
    """This will test to verify all models in config file return valid status code"""
    # Opens the config file and assigns it to config_index
    with open("config.yml", "r") as f:
        config_models = yaml.safe_load(f)["models"]
    for model in config_models:
        response = client.get("/api?input=Where is Paris&model=" + model["name"])
        assert response.status_code == 200


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


def test_streaming(client):
    """This test will confirm that the response is streamed"""
    response = client.get("/api?input=hielo")
    assert response.is_streamed == True


def test_redirect(page: Page):
    """This test makes sure the nav bar works by testing the first navigation link on the playground"""
    page.goto("http://127.0.0.1:5000/playground")
    page.query_selector("nav li:first-child a").click()
    assert page.url == "http://127.0.0.1:5000/"


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
