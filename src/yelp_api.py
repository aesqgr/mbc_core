import requests
import json
import os
import dotenv
yelp_client = os.getenv("YELP_CLIENT_ID")
yelp_key = os.getenv("YELP_API_KEY")
headers = {'Authorization': 'Bearer %s' % yelp_key}
url='https://api.yelp.com/v3/businesses/search'
params = {'term':'pescado','location':'Eixample'}
url='https://api.yelp.com/v3/businesses/search'
req=requests.get(url, params=params, headers=headers)