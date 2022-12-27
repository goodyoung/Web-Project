from flask import Flask, render_template, request, session, g
from web.db import WebProject, exp_manager
import json

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretkeys'
    wp = WebProject.instance()
    em = exp_manager.instance()

    from .views import login_views, main_views, quest_views, myinfo_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(login_views.bp)
    app.register_blueprint(quest_views.bp)
    app.register_blueprint(myinfo_views.bp)

    @app.route('/connectSheet')
    def connectSheet():
        return json.dumps(wp.connect_sheet())

    @app.route('/connectForm')
    def connectForm():
        return json.dumps(wp.connect_form())

    @app.route('/chk_lvup')
    def check_lvup():
        is_lvup = {}
        is_lvup["lv"] = em.check_lvup(g.user["user_id"])
        return json.dumps(is_lvup)

    @app.route('/testpage')
    def test_frame():
        return render_template('frame.html')

    return app