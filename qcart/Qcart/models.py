from datetime import datetime
from Qcart import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # watchlist = db.Column(db.String(100),nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)  # Added subject field
    message = db.Column(db.Text, nullable=False)



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the User model
    items = db.Column(db.String(100))
    prices = db.Column(db.String(100))
    watch7 = db.Column(db.Integer)
    watchSE = db.Column(db.Integer)
    watch3 = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, items={self.items}, prices={self.prices}, watch7={self.watch7}, watchSE={self.watchSE}, watch3={self.watch3}, timestamp={self.timestamp})"
