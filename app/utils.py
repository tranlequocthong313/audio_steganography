import os
from io import BytesIO

from flask import current_app, send_file

from app.file import read


def format_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = size_in_bytes

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def get_file_path(filename):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], filename)


def respond_file(filename):
    file_path = get_file_path(filename)
    return send_file(
        BytesIO(read(file_path)), download_name=filename, as_attachment=True
    )
