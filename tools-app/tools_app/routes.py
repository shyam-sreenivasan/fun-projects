from tools_app.app import app
from flask import render_template, jsonify, request, flash, url_for, redirect
from hashlib import sha256
from tools_app.tools.crypt import encrypt_string, decrypt_string
from tools_app.tools.mergepdfs import merge_pdfs
from tools_app import UPLOAD_FOLDER, MEDIA_BACKUP_PATH
import time
import os
from flask import send_from_directory
from datetime import datetime
import uuid
import threading
from tools_app.tools.youtube.downloader import run_download_youtube
from tools_app.tools.image_util import convert_images_to_pdf
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips # type: ignore
import mimetypes
import calendar
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/crypt", methods=["GET"])
def crytp_page():
    return render_template("crypt.html")

@app.route("/crypt", methods=["POST"])
def encrypt_decrypt():
    try:
        data = request.get_json()
        phrase = data.get("phrase")
        key_str = data.get("key")
        action = data.get("action")

        if not phrase or not key_str or not action:
            return jsonify(result="Missing required fields"), 400

        # Derive 256-bit key from the key string
        key = sha256(key_str.encode()).digest()

        if action == "encrypt":
            result = encrypt_string(key, phrase)
        elif action == "decrypt":
            result = decrypt_string(key, phrase)
        else:
            return jsonify(result="Invalid action"), 400

        return jsonify(result=result)
    
    except Exception as e:
        return jsonify(result=f"Error: {str(e)}"), 500
    

@app.route("/mergepdfs", methods=['GET'])
def mergepdfPage():
    return render_template("merge_pdfs.html")

@app.route("/mergepdfs", methods=["POST"])
def merge_pdfs_endpoint():
    try:
        # Get the list of uploaded PDFs
        pdf_files = request.files.getlist('pdfs')
        
        if not pdf_files:
            return jsonify({"error": "No PDFs uploaded"}), 400
        
        # Generate a unique filename for the merged PDF
        timestamp = str(int(time.time()))
        output_filename = os.path.join(UPLOAD_FOLDER, f"merged_{timestamp}.pdf")
        
        # Call the merge_pdfs function
        merge_pdfs(pdf_files, output_filename)
        
        # Return the filename so that the frontend can request it for download
        return jsonify({"filename": f"merged_{timestamp}.pdf"})
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@app.route('/files', methods=["GET"])
def download_merged_pdf():
    filename = request.args.get('filename')
    
    if not filename:
        return jsonify({"error": "Filename parameter is required"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    print("File path is", file_path)

    # Check if the file exists
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found or not ready, please try again later."}), 404

@app.route('/list_files', methods=['GET'])
def list_files():
    file_list = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith('.part'):
            continue

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        created = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')

        file_list.append({
            "filename": filename,
            "created": created,
            "modified": modified,
            "url": f"/files?filename={filename}"
        })

    file_list.sort(key=lambda x: x["modified"], reverse=True)
    return render_template('list_files.html', files=file_list)

@app.route('/download_youtube', methods=['POST'])
def download_youtube():
    data = request.json
    url = data.get('url')
    mode = data.get('mode')  # audio, video, or both

    if not url or mode not in ['audio', 'video', 'both']:
        return jsonify({'error': 'Invalid input'}), 400

    job_id = str(uuid.uuid4())
    base_name = f"{job_id}"

    thread = threading.Thread(target=run_download_youtube, args=(UPLOAD_FOLDER, url, mode, base_name))
    thread.start()

    # Construct expected file names
    result_files = []
    if mode in ['video', 'both']:
        result_files.append(f"{base_name}.mp4")  # mp4 for video
    if mode in ['audio', 'both']:
        result_files.append(f"{base_name}_audio.mp3")

    # Construct URLs
    file_urls = [f"/files?filename={name}" for name in result_files]

    return jsonify({
        "message": "Download started",
        "files": file_urls
    })

@app.route("/ytdownload", methods=['GET'])
def get_ytdownloader_page():
    return render_template("yt_downloader.html")


@app.route("/image-to-pdf", methods=["GET", "POST"])
def image_to_pdf():
    if request.method == "POST":
        images = request.files.getlist("images")
        if not images:
            return jsonify({"error": "No images uploaded"}), 400

        image_paths = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"image_pdf_{timestamp}.pdf"
        output_path = os.path.join(UPLOAD_FOLDER, base_filename)

        for img in images:
            filepath = os.path.join(UPLOAD_FOLDER, img.filename)
            img.save(filepath)
            image_paths.append(filepath)

        try:
            convert_images_to_pdf(image_paths, output_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({"download_url": f"/files?filename={base_filename}"})
    return render_template("img_to_pdf.html")


@app.route('/delete-file', methods=["POST"])
def delete_file():
    filename = request.form.get('filename')
    if not filename:
        flash("No filename provided.", "danger")
        return redirect(url_for('list_files'))

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect(url_for('list_files'))

def parse_time_to_seconds(time_str):
    """Convert HH:MM:SS to seconds."""
    parts = list(map(int, time_str.strip().split(":")))
    while len(parts) < 3:
        parts.insert(0, 0)  # pad to HH:MM:SS
    h, m, s = parts
    return h * 3600 + m * 60 + s

@app.route('/trim-media', methods=['GET', 'POST'])
def trim_media():
    if request.method == "POST":
        file = request.files.get('media_file')
        start_times = request.form.getlist('start_times')
        end_times = request.form.getlist('end_times')

        if not file or not start_times or not end_times or len(start_times) != len(end_times):
            return jsonify({"error": "Invalid input. Provide a file and matching start/end times."}), 400

        original_filename = file.filename
        ext = os.path.splitext(original_filename)[1]
        input_filename = f"{uuid.uuid4().hex}{ext}"
        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        file.save(input_path)

        mime_type, _ = mimetypes.guess_type(input_path)
        is_audio = mime_type and mime_type.startswith('audio')

        start_seconds = [parse_time_to_seconds(t) for t in start_times]
        end_seconds = [parse_time_to_seconds(t) for t in end_times]

        output_ext = '.mp3' if is_audio else '.mp4'
        output_filename = f"trimmed_{uuid.uuid4().hex}{output_ext}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        def trim_task():
            try:
                if is_audio:
                    clip = AudioFileClip(input_path)
                    segments = [clip.subclipped(s, e) for s, e in zip(start_seconds, end_seconds)]
                    final_clip = concatenate_audioclips(segments)
                    final_clip.write_audiofile(output_path)
                else:
                    clip = VideoFileClip(input_path)
                    segments = [clip.subclipped(s, e) for s, e in zip(start_seconds, end_seconds)]
                    final_clip = concatenate_videoclips(segments)
                    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                clip.close()
                final_clip.close()

            except Exception as e:
                print(f"[ERROR] Background trim task failed: {e}")

        threading.Thread(target=trim_task, daemon=True).start()

        return jsonify({
            "message": "Trimming started.",
            "download_url": url_for('download_merged_pdf', filename=output_filename),
            "filename": output_filename
        })

    return render_template("trim_media.html")

@app.route('/backup-media', methods=['GET'])
def backup_media_form():
    return render_template('backup_media.html')

@app.route('/backup-media', methods=['POST'])
def backup_media():
    files = request.files.getlist('media')
    subfolder = request.form.get('subfolder', '').strip()

    if not files or not any(file.filename for file in files):
        return jsonify({"success": False, "message": "No files provided."}), 400

    # If no subfolder is provided, generate one based on the current month and year
    if not subfolder:
        now = datetime.now()
        subfolder = f"{calendar.month_name[now.month]}-{now.year}"

    # Create a folder for the files under the backup path
    upload_path = os.path.join(MEDIA_BACKUP_PATH, secure_filename(subfolder))
    os.makedirs(upload_path, exist_ok=True)

    saved_files = []
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            dest = os.path.join(upload_path, filename)
            file.save(dest)
            saved_files.append(filename)

    return jsonify({
        "success": True,
        "message": f"{len(saved_files)} file(s) uploaded successfully to: {upload_path}",
        "uploaded_to": upload_path,
        "files": saved_files
    })