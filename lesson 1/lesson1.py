import json
import requests

api_method = 'users.getSubscriptions'
url = f'https://api.vk.com/method/{api_method}'

my_params = {'user_id': '486973140', # Некий Илья Акчурин из Ижевск
             'access_token': 'shabam', # Токен не публикуем =)
             'v': '5.131'}


response = requests.get(url, params = my_params)

with open('subscriptions.json', 'w') as fp:
    json.dump(response.json(), fp)


