from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment1 = db.Column(db.Text, nullable=True)  # allow null
    comment2 = db.Column(db.Text, nullable=True)
    comment3 = db.Column(db.Text, nullable=True)