from app import db

class ShortURL(db.Model):
    __tablename__ = 'shortURL'
    key = db.Column(db.String(10), primary_key=True)
    url = db.Column(db.String(1000))
