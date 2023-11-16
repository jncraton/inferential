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
    """This will test to verify a status for a normal query"""
    response = client.get("/api?input=Where is Paris&model=1")
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


def test_ctransformers_exists():
    """This test will check if ctransformers exist and is working"""
    try:
        from ctransformers import AutoModelForCausalLM

        assert True
    except ImportError:
        assert False, "ctransformers library not found"


def test_ctransformers_working():
    """This test will check if ctransformers model is loaded in app.py"""
    assert isinstance(selected_model, dict)
    assert selected_model.get("backend") == "ctransformers"

    # Check if the ctransformers model can be instantiated
    model_name = selected_model.get("name")
    try:
        llm = AutoModelForCausalLM.from_pretrained(model_name)
        assert True
    except Exception as e:
        assert False, f"Error loading ctransformers model: {e}"


def test_empty_query(page: Page):
    """This will test if the user queries an empty string"""
    page.goto("http://127.0.0.1:5000/playground")
    page.get_by_role("button", name="Submit").click()
    chat_reply = page.locator("#outputResponse")
    expect(chat_reply).to_contain_text("Error: No prompt was provided.")


def test_empty_query_api(client):
    """This will test to verify a status for empty query"""
    response = client.get("/api?input=&model=1")
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
        "/api?input=" +
        ("".join(choice(ascii_lowercase) for i in range(250))) +
        "&model=1"
    )
    assert response.status_code == 413


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
    response = client.get("/api?input=" + "hielo" + "&model=1")
    assert response.is_streamed == True


def test_redirect(browser):
    """This test will test to see if the page will redirect to the playground after a certain amount of time and properly load"""
    page = browser.new_page()
    page.goto("http://127.0.0.1:5000/")
    # Wait for 5 seconds, adjust based on potential wait times
    page.wait_for_url("http://127.0.0.1:5000/playground", timeout=5000)
    assert page.url == "http://127.0.0.1:5000/playground"
