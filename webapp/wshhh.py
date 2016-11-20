import base64
import re

from babel.dates import format_timedelta
from datamodels import User, Attribute, ItemAttribute, Item, Image
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import (LoginManager, UserMixin, login_required,
        login_user, logout_user, current_user)
from PIL import Image as PImage
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "shingedlyh"
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == int(user_id))
    except (ValueError, User.DoesNotExist) as e:
        return None


@app.route("/")
@login_required
def main():
    items = list()
    for item in current_user.items.order_by(Item.created.desc()):
        image = next(iter(item.images))
        attrs = list()
        for attr in Attribute.select().join(ItemAttribute).join(Item).where(
                Item.id == item.id):
            attrs.append(attr)
        items.append((item, image, attrs))
    return render_template("main.html", items=items)


@app.route("/save", methods=["POST"])
@login_required
def save():
    prefix = b"data:image/png;base64,"
    item = Item.create(user=current_user.id)
    # Process the label picture
    data = bytes(request.form["snap2"], "utf8")
    data = data[len(prefix):]
    label_filename = "label_x{}.png".format(item.id)
    with open("static/usercontent/{}".format(label_filename), "wb") as f:
        f.write(base64.decodebytes(data))
    # Process the clothing picture.
    data = bytes(request.form["snap1"], "utf8")
    data = data[len(prefix):]
    fullres_filename = "full_x{}.png".format(item.id)
    with open("static/usercontent/{}".format(fullres_filename), "wb") as f:
        f.write(base64.decodebytes(data))
    thumbnail_filename = make_thumbnail(item.id)
    image = Image.create(item=item.id, thumbnail_filename=thumbnail_filename,
            fullres_filename=fullres_filename)
    return redirect(url_for("main"))


def make_thumbnail(iid):
    fullres_filename = "full_x{}.png".format(iid)
    thumbnail_filename = "thumb_x{}.png".format(iid)
    img = PImage.open("static/usercontent/{}".format(fullres_filename))
    w, h = img.size
    if w > h:
        new_w = int((w / h) * 500)
        new_h = 500
    else:
        new_w = 500
        new_h = int((h / w) * 500)
    img = img.resize((new_w, new_h), resample=PImage.LANCZOS)
    if new_w > new_h:
        half = new_w // 2
        box = (half-249, 0, half+250, 499)
    else:
        half = new_h // 2
        box = (0, half-250, 499, half+249)
    img = img.crop(box)
    img.save("static/usercontent/{}".format(thumbnail_filename))
    return thumbnail_filename


@app.route("/login", methods=["GET", "POST"])
def login_or_signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']        
        next = request.args.get("next", url_for("main"))
        try:
            user = User.get(User.email == email)
        except User.DoesNotExist:
            # Attempt to create a new user.
            valid_email, valid_pw = validate_credentials(email, password)
            if valid_email and valid_pw:
                pw_hash = generate_password_hash(password)
                user = User.create(email=email, pw_hash=pw_hash)
                login_user(user)
                return redirect(next) # TODO security hole.
            else:
                return render_template("login.html", email=email,
                        valid_email=valid_email, valid_pw=valid_pw)
        # We found a user with this e-mail in the DB.
        if check_password_hash(user.pw_hash, password):
            login_user(user)
            return redirect(next)
        else:
            return render_template("login.html", email=email, wrong_pw=True)
    else:
        return render_template("login.html")


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login_or_signup'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_or_signup"))


def validate_credentials(email, password):
    valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", email)
    valid_pw = len(password) >= 6
    return valid_email, valid_pw


def format_dt(dt):
    return format_timedelta(datetime.now() - dt)
app.jinja_env.filters['timedelta'] = format_dt
