from flask import Flask, request, jsonify, send_from_directory, Response, redirect
import os
import string
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory code registry: maps 6-char code -> filename
code_to_file = {}
file_to_code = {}


def generate_code(length=6):
    """Generate a random alphanumeric code (uppercase + digits, no ambiguous chars)."""
    # Exclude ambiguous characters: 0/O, 1/I/L
    chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    while True:
        code = ''.join(random.choices(chars, k=length))
        if code not in code_to_file:
            return code


# Serve frontend
@app.route('/')
def index():
    return send_from_directory('', 'index.html')


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

    # Generate a 6-digit share code
    code = generate_code()
    code_to_file[code] = filename
    file_to_code[filename] = code

    return jsonify({
        "message": "File uploaded successfully",
        "link": f"/download/{filename}",
        "code": code
    })


# Download by code endpoint (short URL)
@app.route('/c/<code>', methods=['GET'])
def download_by_code(code):
    code_upper = code.upper()
    filename = code_to_file.get(code_upper)
    if not filename:
        return jsonify({"error": "Invalid or expired code"}), 404
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Download endpoint (original, keep for backward compatibility)
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Lookup code for a filename (used by frontend)
@app.route('/lookup/<filename>', methods=['GET'])
def lookup_code(filename):
    code = file_to_code.get(filename)
    if not code:
        return jsonify({"error": "No code found"}), 404
    return jsonify({"code": code})


# SEO: robots.txt
@app.route('/robots.txt')
def robots():
    content = """User-agent: *
Allow: /
Sitemap: https://filesharing-ob0e.onrender.com/sitemap.xml
"""
    return Response(content, mimetype='text/plain')


# SEO: sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://filesharing-ob0e.onrender.com/</loc>
    <lastmod>2025-05-25</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    return Response(content, mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True)