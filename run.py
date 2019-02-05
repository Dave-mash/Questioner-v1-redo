from app import create_app
import os
from app.database import InitializeDb

config_name = os.getenv('APP_SETTINGS')
db_url = os.getenv('FLASK_DATABASE_URI')
app, db = create_app(config_name, db_url)

if __name__ == "__main__":
    app.run()
