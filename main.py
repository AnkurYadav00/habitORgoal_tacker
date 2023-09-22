import os
import string
from datetime import datetime
from random import *

import requests

TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")

# Name/Id of the graph
ACTIVITY = "coding"


# TODO : HTTP POST API request
def create_user():
    global TOKEN, USERNAME
    USERNAME = ''.join(choices(list(string.ascii_lowercase), k=6))
    TOKEN = ''.join(choices(list(string.ascii_lowercase + string.digits), k=12))
    print(TOKEN)
    print(USERNAME)
    user_account = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }
    response = requests.post(url="https://pixe.la/v1/users", json=user_account)
    # we can use .json() here as well but we do that incase if we need to use response data, For POST request we do not care about response data.
    # we only care about response success.
    print(response.text)

    with open('Creds.txt', 'w') as file:
        file.write(f"TOKEN: {TOKEN} | USERNAME: {USERNAME}")


# create new user account
create_user()


def create_graph(username, token):
    url = f"https://pixe.la/v1/users/{username}/graphs"
    header = {
        "X-USER-TOKEN": token
    }
    graph_params = {
        "id": ACTIVITY,
        "name": ACTIVITY,
        "unit": "commit",
        "type": "int",
        "color": "sora"
    }
    response = requests.post(url=url, json=graph_params, headers=header)
    print(response.text)


# create graph must be unique
# create_graph(USERNAME, TOKEN)


def update_graph(username, graphId, Token, quantity=1000):
    url = f"https://pixe.la/v1/users/{username}/graphs/{graphId}"
    header = {
        "X-USER-TOKEN": Token
    }
    Data = {
        'date': str(datetime.now().__format__('%Y%m%d'))[:8],
        'quantity': str(quantity),
    }
    response = requests.post(url=url, headers=header, json=Data)
    assert bool(response.json()["isSuccess"])


# pushing/POSTING new data
# update_graph(USERNAME, ACTIVITY, TOKEN)


# TODO : HTTP PUT API request
# PUT to update the data
# DELETE to delete the data

def update_data(username, graphID, Token, date, quantity=1):
    url = f"https://pixe.la/v1/users/{username}/graphs/{graphID}/{date}"
    header = {
        "X-USER-TOKEN": Token
    }
    Data = {
        'quantity': str(quantity),
    }
    response = requests.put(url=url, headers=header, json=Data)
    assert bool(response.json()["isSuccess"])


# update existing data using PUT API request
# update_data(USERNAME, ACTIVITY, TOKEN, '20230921')


# TODO : DELETE API Requests
def delete_data(username, graphID, Token, date):
    url = f"https://pixe.la/v1/users/{username}/graphs/{graphID}/{date}"
    header = {
        "X-USER-TOKEN": Token
    }

    response = requests.delete(url=url, headers=header)
    assert bool(response.json()["isSuccess"])


# delete existing data using DELETE API request
# delete_data(USERNAME, ACTIVITY, TOKEN, '20230922')
