from flask import Flask
import unittest
from app import app
from flask_sqlalchemy import SQLAlchemy
from images.models import Images, ImageGroup

db = SQLAlchemy(app)
db.init_app(app)


TEST_POSTGRES = {
    'user': 'user',
    'pw': 'admin',
    'db': 'db',
    'host': 'localhost',
    'port': '5432',
}


def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % TEST_POSTGRES
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_main_page(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


class FlaskTestCase(unittest.TestCase):
    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()
        im_group = ImageGroup()
        db.session.add(im_group)
        db.session.commit()
        image = Images(img_filename='test.jpg', counter=1, img_data='tets', imagegroup_id=im_group.id)
        db.session.add(image)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_model_exist(self):
        self.assertTrue(db.session.query(Images).filter(Images.img_filename == 'test.jpg').first() is not None)


if __name__ == "__main__":
    unittest.main()