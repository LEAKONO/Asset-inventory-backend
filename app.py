from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db  
from auth import auth
from routes import bp as api_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app) 
db.init_app(app)  
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run()
