# import socket
# from requests import get

# ip = socket.gethostbyname(socket.gethostname())
# print('Your local IP address is: ', ip)

# ip = get('https://api.ipify.org').text
# print('Your public IP address is: ', ip)



# import requests

# print(requests.get("http://ip.jsontest.com").json()['ip'])



import requests
import re

req = requests.get("http://ipconfig.kr")
print(re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])