from flask import Blueprint, render_template, redirect, url_for
from ..db import WebProject

bp = Blueprint('quest', __name__, url_prefix='/quest')
wp = WebProject.instance()

@bp.route('/')
def quest_list():
    return render_template('main/quest_list.html')

@bp.route('/<int:problem_id>')
def problem_show(problem_id):
    sql = "SELECT type FROM problem WHERE id = {0}".format(problem_id)
    problem_type = wp.send_query(sql)[0]["type"]
    if(problem_type=="객관식"):
        sql = "SELECT problem.*, objective.choices, objective.answer FROM problem INNER JOIN objective ON problem.id = objective.id WHERE problem.id = {}".format(problem_id)
    else:
        sql = "SELECT problem.*, subjective.answer FROM problem INNER JOIN subjective ON problem.id = subjective.id WHERE problem.id = {}".format(problem_id)
    res = wp.send_query(sql)[0]

    return render_template("main/quest_show.html", problem_dict=res)