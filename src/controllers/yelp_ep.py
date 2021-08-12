from src.yelp_api import json
from src.yelp_api import headers
from src.yelp_api import requests
from src.app import app


url='https://api.yelp.com/v3/businesses/search'

@app.route('/yelp/<location>')
def index(location):
    params = {'location':location, "sort_by": "rating"}
    req = requests.get(url, params=params, headers=headers)
    return json.loads(req.text)

