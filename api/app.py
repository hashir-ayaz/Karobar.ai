from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/api/upload", methods=["POST"])
def upload_file():
    # Placeholder for file upload logic
    return "File upload endpoint", 200


# this gets the user's query and returns a list of matched top 10 resumes
@app.route("/api/match", methods=["GET"])
def match_resumes():
    # Placeholder for resume matching logic
    return "Resume matching endpoint", 200


if __name__ == "__main__":
    app.run(debug=True)
