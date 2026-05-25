from flask import Flask, request, jsonify, send_from_directory
import os
import random
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory mapping of 6-digit codes to filenames
code_map = {}


def generate_code():
    """Generate a unique 6-digit uppercase alphanumeric code."""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in code_map:
            return code


# Serve frontend
@app.route('/')
def index():
    return send_from_directory('', 'index.html')


# Serve Google Search Console verification file
@app.route('/google17b8c44586d12fd1.html')
def google_verify():
    return send_from_directory('', 'google17b8c44586d12fd1.html')


# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Generate a 6-digit code for easy sharing
    code = generate_code()
    code_map[code] = filename

    return jsonify({
        "message": "File uploaded successfully",
        "link": f"/download/{filename}",
        "code": code
    })


# Download via 6-digit code
@app.route('/c/<code>', methods=['GET'])
def download_by_code(code):
    code = code.upper()
    if code not in code_map:
        return jsonify({"error": "Invalid or expired code"}), 404

    filename = code_map[code]
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Download endpoint (legacy - keeps old links working)
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)