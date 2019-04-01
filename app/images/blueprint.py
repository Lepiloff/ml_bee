import os, sys
from flask import Blueprint, request, jsonify, session, redirect, url_for
import uuid
from werkzeug.utils import secure_filename
from app import db, q


images = Blueprint('images', __name__)


# Added true folder for import functions from true folder
base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(base)

UPLOAD_FOLDER = base + '/uploads'
ALLOWED_EXTENSIONS = set(["jpg"])

from pyolo.detect import run
from images.models import Images, ImageGroup, image_schema, images_schema


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Result with DB
@images.route("/result/<int:imagegroup>")
def results(imagegroup):
    #imagegroup = imagegroup
    images = Images.query.filter_by(imagegroup_id=imagegroup).first()
    result = image_schema.dump(images)
    return jsonify({'images': result.data})


# For DB using
@images.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        result = {}
        # check if the post request has the file part
        if 'file' not in request.files:
            result['response'] = 'No file part'
            return jsonify(result)
        #Check that file type jpg
        for f in request.files.getlist('file'):
            if not allowed_file(f.filename):
                result['responce'] = 'Only JPG file can be used'
                return jsonify(result)
        else:
            new_file_folder = uuid.uuid4().hex
            os.makedirs(UPLOAD_FOLDER + "/" + new_file_folder)
            for f in request.files.getlist('file'):
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, new_file_folder, filename))
            # Add new image folder
            f_img = os.path.join(UPLOAD_FOLDER, new_file_folder)
            #job queue, add RUN function to thread
            job = q.enqueue(run, f_img)
            if job.status == "failed":
                result['response'] = 'Job failed'
                return jsonify(result)
            while job.result is None:
                pass
            else:
                result_img = job.result
                imagegroup = ImageGroup()
                db.session.add(imagegroup)
                db.session.commit()
                for i in result_img:
                    info = job.result[i]
                    filename = (info['name'])
                    count = info["count"]
                    img_data = info['path']
                    new_file = Images(img_filename=filename, counter=count, img_data=img_data, imagegroup_id=imagegroup.id)
                    db.session.add(new_file)
                    db.session.commit()
                #session['result'] = result_img
                return redirect(url_for("images.results", imagegroup=imagegroup.id))
    return ('', 204)


@images.route('/all/', methods=['GET'])
def get_quotes():
    images = Images.query.all()
    result = images_schema.dump(images, many=True)
    return jsonify({'images': result.data})


#Images by id
@images.route('/<int:id>', methods=['GET'])
def return_img(id):
    image = Images.query.get_or_404(id)
    result = image_schema.dump(image)
    return jsonify({'image': result.data})


#Result withot DB
@images.route("/result/")
def result():
    result = session['result']
    return jsonify(result)


#Without DB for test
@images.route('/test', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        result = {}
        # check if the post request has the file part
        if 'file' not in request.files:
            result['response'] = 'No file part'
            return jsonify(result)
        #Check that file type jpg
        for f in request.files.getlist('file'):
            if not allowed_file(f.filename):
                result['responce'] = 'Only JPG file can be used'
                return jsonify(result)
        else:
            new_file_folder = uuid.uuid4().hex
            os.makedirs(UPLOAD_FOLDER + "/" + new_file_folder)
            for f in request.files.getlist('file'):
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, new_file_folder, filename))
            # Add new image folder
            f_img = os.path.join(UPLOAD_FOLDER, new_file_folder)

            #job queue, add RUN function to thread
            job = q.enqueue(run, f_img)
            if job.status == "failed":
                result['response'] = 'Job failed'
                return jsonify(result)
            while job.result is None:
                pass
            else:
                result_img = job.result
                #print(result_img[1])
                session['result'] = result_img #Add dict  of all images with each count values to session
                #return redirect(url_for("result", count=count))
                return redirect(url_for("images.result"))
    #return render_template("index.html")
    return ('', 204)