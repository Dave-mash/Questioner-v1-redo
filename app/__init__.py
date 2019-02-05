from flask import Flask 
from instance.config import app_config
import os

from app.database import InitializeDb

def create_app(config_name='development', db_url=os.getenv('FLASK_DATABASE_URI')):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False

    from app.api.v1.views.meetup_views import v1 as meetup_v1
    from app.api.v1.views.question_views import v1 as question_v1
    from app.api.v1.views.comment_views import v1 as comment_v1
    from app.api.v1.views.user_views import v1 as user_v1

    from app.api.v2.views.question_views import v2 as question_v2
    from app.api.v2.views.meetup_views import v2 as meetup_v2
    from app.api.v2.views.comment_views import v2 as comment_v2
    from app.api.v2.views.user_views import v2 as user_v2

    app.register_blueprint(question_v1)
    app.register_blueprint(meetup_v1)
    app.register_blueprint(comment_v1)
    app.register_blueprint(user_v1)

    app.register_blueprint(user_v2)
    app.register_blueprint(question_v2)
    app.register_blueprint(comment_v2)
    app.register_blueprint(meetup_v2)

    db = InitializeDb(db_url)
    db.create_tables()
    return app, db
