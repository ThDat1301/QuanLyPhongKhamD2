from flask_admin import Admin
from app import app

admin = Admin(app, name='Quản trị phòng khám', template_mode='bootstrap4')