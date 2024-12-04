from flask import Flask, Response, jsonify, make_response, request
import os
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

UPLOAD_FOLDER = './www/root/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for file upload and CSV conversion
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

# Route for handling coordinates (JSON data)
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

        print("Coordinates received:", coordinates)

        response = make_response(
            jsonify({'message': 'Coordinates received successfully', 'data': coordinates}),
            200,
            {"Access-Control-Allow-Origin": "*"}
        )

        return response
    except Exception as e:
        return jsonify({'error': f'Error processing coordinates: {str(e)}'}), 500

# Route to serve static files
def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src, "rb").read()
    except IOError as exc:
        return str(exc)


@app.route("/www/<path:path>")
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), "www", path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)

@app.route('/init-info', methods=['POST', 'OPTIONS'])
def upload_file():
    # Handle OPTIONS preflight request for CORS
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Check if file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 415
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Ensure upload directory exists
    os.makedirs('./uploads', exist_ok=True)
    
    # Save the file
    file.save(f"./uploads/{file.filename}")
    
    # Create response with CORS headers
    response = make_response(jsonify({'message': 'File successfully uploaded'}), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
if __name__ == '__main__':
    app.run(debug=True)
