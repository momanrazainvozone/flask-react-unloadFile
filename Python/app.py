#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from threading import Lock
from collections import defaultdict
import shutil
import uuid
from flask_cors import CORS

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

storage_path: Path = Path(__file__).parent / "storage"
chunk_path: Path = Path(__file__).parent / "chunk"

allow_downloads = False
dropzone_cdn = "https://cdnjs.cloudflare.com/ajax/libs/dropzone"
dropzone_version = "5.7.6"
dropzone_timeout = "120000"
dropzone_max_file_size = "1000000"
dropzone_chunk_size = "10000000"
dropzone_parallel_chunks = "true"
dropzone_force_chunking = "true"

lock = Lock()
chucks = defaultdict(list)
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html", 
                           allow_downloads=allow_downloads, 
                           dropzone_cdn=dropzone_cdn,
                           dropzone_version=dropzone_version,
                           dropzone_timeout=dropzone_timeout,
                           dropzone_max_file_size=dropzone_max_file_size,
                           dropzone_chunk_size=dropzone_chunk_size,
                           dropzone_parallel_chunks=dropzone_parallel_chunks,
                           dropzone_force_chunking=dropzone_force_chunking,
                           )
  
@app.route("/upload", methods=['POST'])
def uploads():
    file = request.files.get("file")
    if not file:
        return "No file provided", 400

    dz_uuid = request.form.get("dzuuid")
    if not dz_uuid:
        # Assume this file has not been chunked
        with open(storage_path / f"{uuid.uuid4()}_{secure_filename(file.filename)}", "wb") as f:
            file.save(f)
        return "File Saved"

    # Chunked download
    try:
        current_chunk = int(request.form["dzchunkindex"])
        total_chunks = int(request.form["dztotalchunkcount"])
    except KeyError as err:
        return f"Not all required fields supplied, missing{err}", 400
    except ValueError:
        return f"Values provided were not in expected format", 400

    save_dir = chunk_path / dz_uuid

    if not save_dir.exists():
        save_dir.mkdir(exist_ok=True, parents=True)

    # Save the individual chunk
    with open(save_dir / str(request.form["dzchunkindex"]), "wb") as f:
        file.save(f)

    # See if we have all the chunks downloaded
    with lock:
        chucks[dz_uuid].append(current_chunk)
        completed = len(chucks[dz_uuid]) == total_chunks

    # Concat all the files into the final file when all are downloaded
    if completed:
        with open(storage_path / f"{dz_uuid}_{secure_filename(file.filename)}", "wb") as f:
            for file_number in range(total_chunks):
                f.write((save_dir / str(file_number)).read_bytes())
        print(f"{file.filename} has been uploaded")
        shutil.rmtree(save_dir)
        
    return "Chunk upload successful"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
