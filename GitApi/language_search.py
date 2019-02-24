# https://api.github.com/search/repositories?q=tetris+language:java&sort=stars&order=desc

import urllib.parse
import requests

# api = 'https://api.github.com/search/repositories?q='
api = 'https://api.github.com/search/repositories?q=java+language:java&sort=stars&order=desc'

# param  = 'java'
# url  = api + urllib.parse.urlencode({'address':param})

json_data = requests.get(api).json()

print('Response length : ', (json_data['total_count']) )
print(len(json_data['items']))
print(json_data['items'][0]['full_name'])

for item in json_data['items']:
    url = item['html_url']
    print(url)