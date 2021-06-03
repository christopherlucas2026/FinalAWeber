from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful_swagger_3 import Api, swagger

from resources.widget import Widget, WidgetItem, WidgetList
from data.db import db

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Flask API for Widgets"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)
api.add_resource(Widget, '/widget')
api.add_resource(WidgetItem, '/widget/<string:name>')
api.add_resource(WidgetList, '/widgets')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
