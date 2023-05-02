from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .model import Workout, User
from . import sql_db

workout = Blueprint("workout", __name__)


@workout.route("/all")
@login_required
def all_workouts():
    page = request.args.get("page", 1, type=int)
    user = User.query.get_or_404(current_user.user_id)
    workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=5)
    return render_template("all_workouts.html", workouts=workouts)


@workout.route("/new")
@login_required
def new_workout():
    return render_template("create_workout.html")

@workout.route("/new", methods=["POST"])
@login_required
def new_workout_post():
    print(list(request.form.values()))
    pushups, comment = list(request.form.values())
    workout_obj = Workout(pushups_count=pushups, comment=comment, user_id=current_user.user_id)
    sql_db.session.add(workout_obj)
    sql_db.session.commit()
    flash("workout added successfully")
    return redirect(url_for("workout.all_workouts"))

@workout.route("/workout/<int:workout_id>/update", methods=["GET", "POST"])
@login_required
def update_workout(workout_id):
    workout_obj = Workout.query.get_or_404(workout_id)
    if request.method == "POST":
        workout_obj.pushups_count = request.form["pushups"]
        workout_obj.comments = request.form["comment"]
        sql_db.session.commit()
        flash("workout updated successfully")
        return redirect(url_for("workout.all_workouts"))
    
    return render_template("update_workout.html", workout_obj=workout_obj)

@workout.route("/workout/<int:workout_id>/delete")
@login_required
def delete_workout(workout_id):
    workout_obj = Workout.query.get_or_404(workout_id)
    sql_db.session.delete(workout_obj)
    sql_db.session.commit()
    flash("workout deleted successfully")
    return redirect(url_for("workout.all_workouts"))