from app import app, db
from app.models import City, User, Capability, Need, Notification, Message


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'City': City, 'User': User, 'Capability': Capability,
            'Need': Need, 'Message': Message, 'Notification': Notification}