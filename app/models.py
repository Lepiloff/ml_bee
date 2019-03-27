from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

ma = Marshmallow()


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    img_filename = db.Column(db.String())
    counter = db.Column(db.Integer(), default=0)
    img_data = db.Column(db.String(264), unique=False)
    creation_date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<image id={},img_filename={},img_data={} >'.format(self.id, self.img_filename, self.img_data)

class ImageSchema(ma.Schema):
    id = fields.Integer()
    img_filename = fields.String(required=True)
    counter = fields.Integer()

images_schema = ImageSchema(many=True)
image_schema = ImageSchema()