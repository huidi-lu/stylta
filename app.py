import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'do', 'ado'}

app = Flask(__name__)

# Limit the maximum allowed payload to one megabyte
app.config['MAX_CONTENT_LENGTH'] = 1e6
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="uploads", build_only=True
)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def filetype_is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def serve_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/')
def index():
    return render_template("index.html")

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
        flash('Invalid file!')
        return redirect('/')

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('uploads', name=filename))


if __name__ == "__main__":
    app.run()