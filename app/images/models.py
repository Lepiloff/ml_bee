from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

ma = Marshmallow()


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_filename = db.Column(db.String())
    counter = db.Column(db.Integer(), default=0)
    img_data = db.Column(db.String(264), unique=False)
    imagegroup_id = db.Column(db.Integer, db.ForeignKey('imagegroup.id', ondelete='CASCADE'), nullable=False)
    imagegroup = db.relationship('ImageGroup', backref=db.backref('images', lazy=True))

    def __repr__(self):
        return '<image id={},img_filename={},img_data={} >'.format(self.id, self.img_filename, self.img_data)

class ImageGroup(db.Model):
    __tablename__ = 'imagegroup'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class ImageSchema(ma.Schema):
    id = fields.Integer()
    img_filename = fields.String(required=True)
    counter = fields.Integer()


images_schema = ImageSchema(many=True)
image_schema = ImageSchema()




