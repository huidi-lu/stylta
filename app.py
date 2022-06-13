import os
from flask import Flask, flash, request, redirect, render_template
from flask_session import Session
import uuid

from checker import Checker


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'do', 'ado'}

app = Flask(__name__)

# Limit the maximum allowed payload to one megabyte
app.config['MAX_CONTENT_LENGTH'] = 1e6
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def filetype_is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def on_not_found_error(e):
    flash(e)
    return redirect("/")

@app.route('/upload_and_check', methods=['POST'])
def main():
    # check if the post request has the file part.
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    file = request.files.get("file")
    if not file or file.filename == '':
        flash('No file!')
        return redirect('/')

    if not filetype_is_allowed(file.filename):
        flash('Accepting .do files only!')
        return redirect('/')

    filename = uuid.uuid4().hex
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(f'/result/{filename}', code=303)

@app.route('/result/<filename>')
def show_result(filename=None):
    path2file = os.path.join(UPLOAD_FOLDER, filename)
    if filename and os.path.exists(path2file):
        with open(path2file) as codefile:
            try:
                codelines = codefile.read().splitlines()
            except Exception:
                codelines = ["",]
        os.remove(path2file)
        return render_template("result.html", codelines = codelines)
    else:
        flash('Result has been deleted or does not exist.')
        return redirect('/', code=307)


# if __name__ == "__main__":
#     app.run()