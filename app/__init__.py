from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt

def create_app(config_class = Config):
    #Initializes the core Flask application object
    app = Flask(__name__)

    #app.config.from_object reads all uppercase variables from our Config class
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models
    #register blueprints (similar to app.use('/api', router) in express)
    from app.routes.main import main_bp
    from app.routes.posts import posts_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)

    return app