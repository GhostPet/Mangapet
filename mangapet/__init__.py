from flask import Flask

import importlib

from flask_login import current_user

from .extensions import *
from .models import *
from .views import Blueprints

def create_app(config_file='./settings.py'):
	app = Flask(__name__)
	app.config.from_pyfile(config_file)
	
	# Extensions

	## Database & Migrate & Models
	db.init_app(app)
	migrate.init_app(app, db)
	with app.app_context():
		db.create_all()
		
	## Login Manager
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(user_id)

	# Views
	for name, module_name in Blueprints.items():
		module_path = f"{__package__}.{module_name}"
		module = importlib.import_module(module_path)
		app.register_blueprint(getattr(module, name))

	@app.context_processor
	def base_context():
		if current_user.is_authenticated:
			user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
			return dict(title='MangaPet', user=current_user, user_permissions=user_permissions)
		return dict(title='MangaPet')

	return app