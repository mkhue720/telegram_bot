import requests

url = "https://open-weather13.p.rapidapi.com/city/Hanoi/EN"

headers = {
	"X-RapidAPI-Key": "2efa3d7148msh9f69e8f4a6d2e77p184a7djsn37f85be80a0b",
	"X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())