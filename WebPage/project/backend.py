from flask import Flask, render_template, request
from db import WebProject

def create_app():
    app = Flask(__name__)
    wp = WebProject()

    @app.route('/')
    def problem_list():
        return render_template("problem_list.html")

    @app.route('/runSQL', methods=['POST'])
    def run_sql():
        params = request.get_json()
        sql = params["query"]
        return wp.send_query(sql)

    @app.route('/connectSheet')
    def connectSheet():
        return wp.connect_sheet() 

    @app.route('/problem/<int:problem_id>')
    def problem_show(problem_id):
        sql = "SELECT type FROM problem WHERE id = {0}".format(problem_id)
        problem_type = wp.send_query(sql)[0]["type"]
        if(problem_type=="객관식"):
            sql = "SELECT problem.*, objective.choices, objective.answer FROM problem INNER JOIN objective ON problem.id = objective.id WHERE problem.id = {}".format(problem_id)
        else:
            sql = "SELECT problem.*, subjective.answer FROM problem INNER JOIN subjective ON problem.id = subjective.id WHERE problem.id = {}".format(problem_id)
        res = wp.send_query(sql)[0]

        return render_template("problem_show.html", problem_dict=res)

    return app