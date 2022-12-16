from flask import Flask, render_template
from db import WebProject

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def problem_list():
        return render_template("problem_list.html")

    # @app.route('/runSQL', methods=['POST'])
    # def run_sql():
    #     sql = requests.args.get("query")
    #     wp = WebProject()
    #     return wb.send_query(sql)

    return app