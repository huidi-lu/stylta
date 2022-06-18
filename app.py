import os
from flask import Flask, flash, request, redirect, render_template
from flask_session import Session
import uuid

from checker import Checker, is_comment, is_empty

from waitress import serve


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'do', 'ado'}

app = Flask(__name__)

# Limit the maximum allowed payload to five megabytes
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
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

@app.errorhandler(413)
def on_file_oversize(e):
    flash("Maximum allowed filesize is 5 megabytes.")
    return redirect("/")

@app.route('/upload_and_check', methods=['POST'])
def main():
    # Check if the post request has the file part
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    file = request.files.get("file")
    if not file or file.filename == '':
        flash('No file!')
        return redirect('/')

    # Ensure the file is Stata .do file
    if not filetype_is_allowed(file.filename):
        flash('Accepting .do files only!')
        return redirect('/')

    # Unique (temporary) name for the file
    filename = uuid.uuid4().hex

    # Create the uploads folder if it does not exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    # Save the uploaded file for analysis
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(f'/result/{filename}', code=303)

@app.route('/result/<filename>')
def show_result(filename=None):
    path2file = os.path.join(UPLOAD_FOLDER, filename)

    # Check if file exists, else go to homepage
    if filename and os.path.exists(path2file):
        # Load the file, and split the file by physical lines
        with open(path2file) as codefile:
            try:
                codelines = codefile.read().splitlines()
            except Exception:
                codelines = ["",]
        
        # Delete the file if loaded in memory
        os.remove(path2file)

        # Collect lines that are not blank
        nonempty_lines = [line for line in codelines if not is_empty(line)]

        # Collect comment lines
        comment_lines = [line for line in nonempty_lines if is_comment(line)]

        # Count the number of comment lines
        n_comment_lines = len(comment_lines)

        # The number of command lines equals the total lines of code minus lines of comment
        n_command_lines = len(nonempty_lines) - n_comment_lines

        # Render the results page
        return render_template("result.html",
                               n_command_lines = n_command_lines,
                               n_comment_lines = n_comment_lines,
                               codelines = codelines)
    # If file does not exist (or has been deleted), raise an alert
    else:
        flash('Result has been deleted or does not exist.')
        return redirect('/', code=307)


# if __name__ == "__main__":
#     serve(app, max_request_body_size=10 * 1024 * 1024)