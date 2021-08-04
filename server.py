from src.app import app
import src.controllers.general_endpoints
from config import PORT

app.run("0.0.0.0", PORT, debug=True)