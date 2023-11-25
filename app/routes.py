import os

from flask import render_template, request, redirect, session, flash, url_for, jsonify

from app import router
from app.steganography import Steganography, header_lengths
from app.utils import format_size, get_file_path, respond_file
from app.file import write

import time


@router.get("/")
@router.get("/home")
@router.get("/embed")
def embed_page():
    return render_template(
        "embed.html", embedded_info=session.get("embedded_info"), active_tab="embed"
    )


@router.get("/extract")
def extract_page():
    return render_template(
        "extract.html",
        extracted_info=session.get("extracted_info"),
        active_tab="extract",
    )


@router.post("/embed")
def embed():
    carrier_filename = request.files["carrier"].filename
    hidden_filename = request.files["data"].filename
    file_format = "wav"
    carrier_bytes = bytearray(request.files["carrier"].stream.read())
    hidden_bytes = bytearray(request.files["data"].stream.read())

    steganography = Steganography()
    embedded_bytes = None
    try:
        start_time = time.time()
        embedded_bytes = steganography.embed(
            hidden_bytes,
            carrier_bytes,
            hidden_filename,
            skipped_bytes=header_lengths[file_format] + 1,
        )
        print("--- embed %s seconds ---" % (time.time() - start_time))
    except OverflowError as e:
        flash(str(e), category="danger")
        return redirect(url_for(".embed_page"))
    except Exception as e:
        flash("Internal server error.", category="danger")
        return redirect(url_for(".embed_page"))

    write(get_file_path(carrier_filename), embedded_bytes)

    if embedded_bytes:
        session["embedded_info"] = {
            "filename": carrier_filename,
            "size": format_size(len(embedded_bytes)),
        }
    return redirect(url_for(".embed_page"))


@router.post("/extract")
def extract():
    file_format = "wav"
    carrier_bytes = bytearray(request.files["carrier"].stream.read())

    steganography = Steganography()
    info = None
    try:
        start_time = time.time()
        info = steganography.extract(carrier_bytes, header_lengths[file_format] + 1)
        print("--- extract %s seconds ---" % (time.time() - start_time))
    except ValueError as e:
        flash(str(e), category="danger")
        return redirect(url_for(".extract_page"))
    except Exception as e:
        flash("Internal server error.", category="danger")
        return redirect(url_for(".extract_page"))

    filename = info["filename"].decode(encoding="utf-8")

    write(get_file_path(filename), info["data"])

    session["extracted_info"] = {
        "filename": filename,
        "size": format_size(len(info["data"])),
    }

    return redirect(url_for(".extract_page"))


@router.get("/download/<active_tab>/<filename>")
def download(active_tab, filename):
    try:
        response = respond_file(filename)

        if active_tab == "embed":
            del session["embedded_info"]
        elif active_tab == "extract":
            del session["extracted_info"]

        os.remove(get_file_path(filename))

        flash("Downloaded successfully.", category="success")
        return response, 200
    except:
        flash("Internal server error.", category="error")
        return jsonify({"message": "Internal server error"}), 500
