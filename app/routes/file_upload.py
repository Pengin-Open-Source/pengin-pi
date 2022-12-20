from flask import Blueprint, redirect, request
from app.util.s3 import upload_file_to_s3
from werkzeug.utils import secure_filename
from app import create_app

app = create_app()

file_upload_blueprint = Blueprint('file_upload_blueprint',
                                  __name__, url_prefix="/upload")


@file_upload_blueprint.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file key in request.files"

    file = request.files["file"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/")
