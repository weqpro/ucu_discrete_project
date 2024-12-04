from flask import Flask, Response, jsonify, request
import os
import csv

app = Flask(__name__)


@app.route("/")
def home():
    return "Home"

UPLOAD_FOLDER = './www/root/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/set-grid', methods=['POST'])
def set_grid():
    if 'file' not in request.files:
        return jsonify({'error': 'File not provided'}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)

    csv_path = os.path.splitext(file_path)[0] + '.csv'
    try:
        with open(file_path, 'r') as input_file, open(csv_path, 'w', newline='') as output_file:
            reader = input_file.readlines()
            writer = csv.writer(output_file)

            for line in reader:
                writer.writerow([line.strip()])

        return jsonify({'message': 'File processed and saved as CSV', 'csv_file': csv_path}), 200
    except Exception as e:
        return jsonify({'error': f'Error processing the file: {str(e)}'}), 500

@app.route('/init-info', methods=['POST'])
def init_info():
    data = request.get_json()
    required_fields = ['startX', 'startY', 'endX', 'endY', 'step']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        coordinates = {
            'startX': data['startX'],
            'startY': data['startY'],
            'endX': data['endX'],
            'endY': data['endY'],
            'step': data['step']
        }
        return jsonify({'message': 'Coordinates received successfully', 'data': coordinates}), 200
    except Exception as e:
        return jsonify({'error': f'Error processing coordinates: {str(e)}'}), 500


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src, "rb").read()
    except IOError as exc:
        return str(exc)


#  @app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def get_resource(path):  # pragma: no cover
    print("RAN")
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), "www", "root", path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)
