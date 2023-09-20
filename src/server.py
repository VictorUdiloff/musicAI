from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
def test():
    return render_template("site.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        audio_file = request.files['audiofile']
        if audio_file:
            filename = secure_filename(audio_file.filename)  # You should import secure_filename
            file_path = os.path.join('uploads', filename)  # Choose your desired path to save the file
            audio_file.save(file_path)
            return jsonify({'message': 'File uploaded successfully'})
        else:
            return jsonify({'error': 'No file provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run()