from flask import Flask, session, url_for, request, redirect, render_template
from config import Configuration
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import rq_dashboard


app = Flask(__name__)
app.config.from_object(Configuration)

###RQ DASHBOARD

#Autentificate for rq access
@rq_dashboard.blueprint.before_request
def check_auth():
    if not session.get('pass', None) == app.config.get("RQ_PASS"):
        return redirect(url_for('rq_auth'))


@app.route("/auth", methods =["POST", "GET"])
def rq_auth():
    if request.method == 'POST':
        admin = request.form['password']
        if admin == 'bee_master':
            session['pass'] = admin
            return "GOD JOB"
    return render_template('rq_auth.html')

app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
###

db = SQLAlchemy(app)
sess = Session()

sess.init_app(app)
db.init_app(app)

#Connect to redis DB and worker create
from redis import Redis
from rq import Queue
q = Queue(connection=Redis())

#Blueprint
from images.blueprint import images
app.register_blueprint(images, url_prefix='/images')


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")
    #return ('', 204)