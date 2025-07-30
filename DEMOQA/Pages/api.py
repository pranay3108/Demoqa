import requests
url="https://google.com"
try:
    response=requests.get(url)
    if response.status_code==201:
        print(url+"successfull")
    else:
        print("fail")
except requests.exceptions.RequestException as exe:
    print("exception")
