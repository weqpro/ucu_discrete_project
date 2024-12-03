from flask import Flask, Response
import os.path

app = Flask(__name__)


@app.route("/")
def home():
    return "Home"


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
