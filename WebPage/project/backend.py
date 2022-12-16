from flask import Flask, render_template, request
from db import WebProject

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def problem_list():
        return render_template("problem_list.html")

    @app.route('/runSQL', methods=['POST'])
    def run_sql():
        params = request.get_json()
        sql = params["query"]
        wp = WebProject()
        return wp.send_query(sql)

    return app