from flask import Flask
from config import Configuration
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)
sess = Session()

sess.init_app(app)
db.init_app(app)

#Connect to redis DB
from redis import Redis
from rq import Queue
q = Queue(connection=Redis())

#Blueprint
from images.blueprint import images
app.register_blueprint(images, url_prefix='/images')


@app.route('/', methods=['GET'])
def index():
    return ('', 204)