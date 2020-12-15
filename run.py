import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_recipes")
def get_recipes():
    recipe =mongo.db.recipe.find()
    return render_template(get_recipes.html, recipes=recipe)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/listings')
def listings():
    return render_template("listings.html")


app.config["IMAGES"] = "/workspace/PRO3-RecipeCloud/static/img/uploads"
app.config["ALLOWED_IMAGE"] = ["PNG", "JPG", "JPEG"]


def allow_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE"]:
        return True
    else:
        return False


@app.route("/input", methods=["GET", "POST"])
def input():

    if request.method == "POST":

        if request.files:
            image = request.files["image"]

            if image.filename == "":
                print("Image needs a filename")
                return redirect(request.url)

            if not allow_image(image.filename):
                print("That file extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGES"], filename))

            print("Saved Image")

            return redirect(request.url)

    return render_template("input.html")


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
