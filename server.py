from src.app import app
import src.controllers.population_ep
import src.controllers.yelp_ep
from config import PORT
import sys
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/")
sys.path.append("/Users/angel/Documents/MidBootcamp/mbc_core/src/")
app.run("0.0.0.0", PORT, debug=True)