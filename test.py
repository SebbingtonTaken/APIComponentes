import requests

# BASE = "http://18.216.216.219/"
BASE = "http://127.0.0.1:5000/"


response = requests.put(BASE + "helloworld/1",{"desc": "Numbah 1"})
print(response.json())
print(BASE)