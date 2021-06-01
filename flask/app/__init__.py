from flask import Flask
from flask_jwt_extended import JWTManager

from . import config, bookmark, db, auth

def create_app(test_config=None):
  """Application factory

  Args:
      test_config (Object, optional): Testing configuration. Defaults to None.

  Returns:
      app: Return app
  """    
  app = Flask(__name__)
  
  if test_config is None:
    app.config.from_object(config.Config)
  else:
    app.config.from_object(config.TestingConfig)
  
  JWTManager(app)
  
  app.app_context().push()
  
  # Initialized database 
  db.init_db()
  db.seed()
  
  # Blueprints for routes
  app.register_blueprint(bookmark.bp)
  app.register_blueprint(auth.register_bp)
  app.register_blueprint(auth.login_bp)
  
  @app.route("/", methods=["GET"])
  def index():
    return "Hello from '/'"  
  
  
  return app