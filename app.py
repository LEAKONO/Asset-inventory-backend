import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth
from routes import bp as inventory_bp  

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_database_nroj_user:8wQJyARUpRxFdZ5TlaH4i5YxGgpKq7mT@dpg-cq3sk6qju9rs739k6en0-a.oregon-postgres.render.com/asset_inventory_db'
app.config.from_object(Config)
# Initialize extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(inventory_bp, url_prefix='/inventory')  

if __name__ == '__main__':
    app.run(debug=True)
