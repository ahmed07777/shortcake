'''This module contains the database model definition only.'''

from app import db

class ShortURL(db.Model):
    '''This class represents the sole database table of the application,
       which serves to associate short URLs with long ones. The short URL
       key is used as the database primary key, because these have to be
       unique anyway.
    '''
    __tablename__ = 'shortURL'
    key = db.Column(db.String(10), primary_key=True)
    url = db.Column(db.String(1000))
