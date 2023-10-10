import requests
url = "http://127.0.0.1:5000/"
response = requests.post(url)
print(response.json()) #looks for json 
#assert(response.status_code == 200)