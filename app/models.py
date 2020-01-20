from app import db

class ShortURL(db.Model):
    key = db.Column(db.String(10), primary_key=True)
    url = db.Column(db.String(1000))
