from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#This creates the comments table in the database
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment1 = db.Column(db.Text, nullable=True)  
    comment2 = db.Column(db.Text, nullable=True)
    comment3 = db.Column(db.Text, nullable=True)