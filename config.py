import os
import dotenv
dotenv.load_dotenv()
PORT = os.getenv("PORT")
DBURL = os.getenv("DBURL")

local_ip = 'http://192.168.88.243'
geo_districts = "https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.geojson"
geo_hoods = "https://raw.githubusercontent.com/martgnz/bcn-geodata/master/barris/barris.geojson"