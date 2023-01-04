from flask_login import LoginManager

from app.auth.models import UserAuth


def create_login_manager():
    """"""
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    return login_manager


login_manager = create_login_manager()


@login_manager.user_loader
def load_user(user_id):
    """Load user."""
    return UserAuth.select().where(UserAuth.id == user_id).first()
