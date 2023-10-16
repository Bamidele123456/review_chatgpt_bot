# models
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RequestData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topography = db.Column(db.String(100))
    vegetation = db.Column(db.String(200))
    gfeatures = db.Column(db.String(200))
    climate = db.Column(db.String(200))
    wildlife = db.Column(db.String(200))
    building = db.Column(db.String(200))
    scent = db.Column(db.String(200))
    bodies = db.Column(db.String(200))
    terrain = db.Column(db.String(200))
    responses = db.Column(db.String(200))

class RequestData2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target1 = db.Column(db.String(100))
    target2 = db.Column(db.String(100))







