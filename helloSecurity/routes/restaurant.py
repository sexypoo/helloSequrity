from flask import Blueprint, render_template, request, redirect, url_for
from helloSecurity import db
from helloSecurity.models import Restaurant, Tag, RestaurantTag, TagCategory

from datetime import time

bp = Blueprint("restaurants", __name__, url_prefix="/restaurants")

# READ
@bp.route("/")
def index():
    restaurants = Restaurant.query.order_by(Restaurant.id.desc()).all()
    return render_template("restaurants/index.html", restaurants=restaurants)

# CREATE
@bp.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        start_time = time.fromisoformat(request.form["start_hour"])
        end_time   = time.fromisoformat(request.form["end_hour"])

        r = Restaurant(
            name=request.form["name"],
            address=request.form["address"],
            description=request.form["description"],
            rating=int(request.form["rating"]),
            start_hour=start_time,
            end_hour=end_time,
            break_time=request.form["breaktime"]
        )

        db.session.add(r)     
        db.session.flush()

        tag_ids = map(int, request.form.getlist("tags"))
        db.session.add_all(
            [RestaurantTag(restaurant_id=r.id, tag_id=tid) for tid in tag_ids]
        )                      

        db.session.commit()
        return redirect(url_for("restaurants.index"))

    categories = TagCategory.query.order_by(TagCategory.id).all()
    return render_template("restaurants/form.html",
                           tags=[],               # ← 안 써도 되지만 호환용
                           categories=categories)

# UPDATE ─ 수정
@bp.route("/<int:r_id>/edit", methods=["GET", "POST"])
def edit(r_id):
    r = Restaurant.query.get_or_404(r_id)

    if request.method == "POST":

        start_str = request.form["start_hour"]
        end_str   = request.form["end_hour"]

        start_time = time.fromisoformat(start_str)
        end_time   = time.fromisoformat(end_str)

        r.name = request.form["name"]
        r.address = request.form["address"]
        r.description = request.form["description"]
        r.rating = request.form['rating']
        r.start_hour = start_time
        r.end_hour = end_time
        r.break_time = request.form['breaktime']

        RestaurantTag.query.filter_by(restaurant_id=r.id).delete()
        for tag_id in request.form.getlist("tags"):
            db.session.add(RestaurantTag(
                restaurant_id=r.id,
                tag_id=int(tag_id)
            ))

        db.session.commit()
        return redirect(url_for("restaurants.index"))

    categories = TagCategory.query.order_by(TagCategory.id).all()
    attached = {rel.tag_id for rel in r.tags} # 수정 폼에 미리 체크되어있음
    return render_template("restaurants/form.html",
                           restaurant=r,
                           categories=categories,
                           attached=attached)

# DELETE ─ 삭제
@bp.route("/<int:r_id>/delete", methods=["POST"])
def delete(r_id):
    r = Restaurant.query.get_or_404(r_id)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for("restaurants.index"))