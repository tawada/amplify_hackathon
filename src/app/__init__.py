import os
from flask import Flask, render_template, flash
from app.views.add import app_add
from app.views.solve import app_solve
from app.views.download import app_download


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SESSION_KEY', 'super secret key')


app.register_blueprint(app_add, url_prefix='/add')
app.register_blueprint(app_solve, url_prefix='/solve')
app.register_blueprint(app_download, url_prefix='/app_download')


@app.route('/', methods=['GET', 'POST'])
def index():
    if not os.environ.get('AMPLIFY_TOKEN'):
        flash("AMPLIFY TOKENが登録されていません", "failed")
    return render_template('index.html')
