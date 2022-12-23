from flask import Blueprint, render_template, redirect, url_for, request, session, g
from ..db import WebProject
from markupsafe import Markup
import json

bp = Blueprint('quest', __name__, url_prefix='/quest')
wp = WebProject.instance()

@bp.route('/')
def quest_list():
    category_data = {}
    category_data["list"] = wp.send_query("SELECT category, COUNT(category) AS n FROM problem GROUP BY category ORDER BY category")
    category_data["total"] = wp.send_query("SELECT COUNT(*) AS count FROM problem")[0]["count"]

    problem_list = wp.send_query("""
    SELECT problem.id, problem.category, (CASE solved WHEN 1 THEN 'solved' WHEN 0 THEN 'solving' ELSE 'unsolved' END) as status 
    FROM problem LEFT JOIN solving ON problem.id = solving.problem_id AND user_id='{}' 
    ORDER BY problem.id
    """.format(g.user["user_id"]))
    return render_template('main/quest_list.html', category_data = category_data, problem_list = problem_list)

@bp.route('/<int:problem_id>', methods=['GET', 'POST'])
def problem_show(problem_id):
    if(request.method == "POST"):
        params = request.get_json()
        # send = {}

        result = wp.send_query("SELECT CASE WHEN answer = '{}' THEN TRUE ELSE FALSE END AS success FROM {} WHERE id = {}".format(params["answer"], params["type"], params["problem_id"]))

        is_exist = wp.send_query("SELECT EXISTS (SELECT * FROM solving WHERE user_id = '{}' AND problem_id = {}) as success".format(g.user["user_id"], params["problem_id"]))

        if(is_exist[0]["success"]):
            wp.send_query("UPDATE solving SET solved = {} WHERE user_id = '{}' AND problem_id = {}".format(result[0]["success"], g.user["user_id"], params["problem_id"]), commit=True)
        else:
            wp.send_query("INSERT INTO solving(solved, user_id, problem_id) VALUES ('{}', '{}', {})".format(result[0]["success"], g.user["user_id"], params["problem_id"]), commit=True)
        
        # send["result"] = result[0]["result"]
        

        return json.dumps(result)
        
    
    problem_data = {}

    problem_data["status"] = wp.send_query("""
    SELECT (CASE solved WHEN 1 THEN 'solved' WHEN 0 THEN 'solving' ELSE 'unsolved' END) as status 
    FROM problem LEFT JOIN solving ON problem.id = solving.problem_id AND user_id = '{}' WHERE id = '{}'
    """.format(g.user["user_id"], problem_id))[0]["status"]

    problem_type = wp.send_query("SELECT type FROM problem WHERE id = {0}".format(problem_id))[0]["type"]
    if(problem_type=="객관식"):
        sql = "SELECT problem.*, objective.choices, objective.answer FROM problem INNER JOIN objective ON problem.id = objective.id WHERE problem.id = {}".format(problem_id)
    else:
        sql = "SELECT problem.*, subjective.answer FROM problem INNER JOIN subjective ON problem.id = subjective.id WHERE problem.id = {}".format(problem_id)
    
    problem_data["problem"] = wp.send_query(sql)[0]

    print(problem_data["problem"])

    for key, val in problem_data["problem"].items():
        if(type(val)==str):
            val = val.replace("\'\'", "\'")
            val = val.replace("\"\"", "\"")
            problem_data["problem"][key] = val
            
    # problem_data["problem"]["content"] = problem_data["problem"]["content"].replace("\n", "<br>")
    # problem_data["problem"]["explanation"] = problem_data["problem"]["explanation"].replace("\n", "<br>")

    print(problem_data["problem"])

    return render_template("main/quest_show.html", problem_data=problem_data)