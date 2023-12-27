from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        tags = request.form["tags"]
        problem_id = request.form["problem_id"]
        tags = tags.strip().split(" ")
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_location = f"{app.config['UPLOAD_FOLDER']}/{filename}"
            file.save(file_location)
        else:
            flash("no file is selected")
            return redirect(request.url)

        data = {
            "name": name,
            "date": date,
            "tags": tags,
            "problem_id": problem_id,
            "file_location": file_location,
        }
        session["data"] = data
        return redirect(url_for("draw"))
    return render_template("form.html")


@app.route("/draw")
def draw():
    data = session.get("data")
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.config["SESSION_TYPE"] = "filesystem"

    app.debug = True
    app.run()
