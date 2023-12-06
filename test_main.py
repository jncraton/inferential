import yaml
import pytest
from app import app
from playwright.sync_api import Page, expect
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


def test_empty_query_api(client):
    """This will test to verify a status for empty query"""
    response = client.get("/api?input=")
    assert response.status_code == 400


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
        f"Error: The prompt exceeded length of {config_models[0]['max_prompt_length']} ."
    )


def test_query_too_big_api(client):
    """This will test verify status code for a too big query"""
    with open("config.yml", "r") as f:
        config_models = yaml.safe_load(f)["models"]
    for model in config_models:
        response = client.get(f"/api?input={'a ' * model['max_prompt_length']}")
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
