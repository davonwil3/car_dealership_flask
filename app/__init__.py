
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .authentication.routes import auth
from models import db , login_manager
from .api.routes import site
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__, template_folder='./site/site_templates')
CORS(app)
jwt = JWTManager(app)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.py')
app.config['JWT_SECRET_KEY'] = '123456789'
app.config.from_pyfile(config_path)
login_manager.init_app(app)
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(site)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)

