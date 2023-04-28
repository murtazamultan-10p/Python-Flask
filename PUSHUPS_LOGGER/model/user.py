from .. import sql_db

class User(sql_db.Model):
    user_id = sql_db.Column(sql_db.Integer, primary_key=True)
    email = sql_db.Column(sql_db.String(100), unique=True)
    name = sql_db.Column(sql_db.String(100))
    password = sql_db.Column(sql_db.String(100))
    workouts = sql_db.relationship('Workout', backref='author', lazy=True)