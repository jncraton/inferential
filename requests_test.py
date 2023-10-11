import requests
url = "http://127.0.0.1:5000/"
response = requests.post(url + "LLM/What is 2 + 2")
print(response.json()) #looks for json 
