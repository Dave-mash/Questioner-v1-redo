from flask import Flask 
from instance.config import app_config
from app.api.v1.views.meetup_views import v1 as meetup_v1
from app.api.v1.views.question_views import v1 as question_v1
from app.api.v1.views.comment_views import v1 as comment_v1
from app.api.v1.views.user_views import v1 as user_v1

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(question_v1)
    app.register_blueprint(meetup_v1)
    app.register_blueprint(comment_v1)
    app.register_blueprint(user_v1)

    return app