from datetime import datetime
from .. import sql_db

class Workout(sql_db.Model):
    workout_id = sql_db.Column(sql_db.Integer, primary_key=True)
    pushups_count = sql_db.Column(sql_db.Integer, nullable=False)
    comments = sql_db.Column(sql_db.Text, nullable=False)
    created_date = sql_db.Column(sql_db.Date, default=datetime.now, nullable=False)
    user_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('user.user_id'), nullable=False)

    def __init__(self, pushups_count, comment, user_id):
        self.pushups_count = pushups_count
        self.comments = comment
        self.user_id = user_id