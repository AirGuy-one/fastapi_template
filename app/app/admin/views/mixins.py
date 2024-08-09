from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.models.user import UserRole


class CustomModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.super_user
