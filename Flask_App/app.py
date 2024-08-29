from flask import Flask
from models import db, bcrypt
from routes import auth, api
from schemas import ma
from config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)


    