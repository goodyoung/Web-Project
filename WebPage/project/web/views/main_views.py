from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main_page():
    log = session.get('logged_in')
    if log:
        # 로그인 중이면
        return render_template('main/main_page.html')
    else:
        # 로그인 정보가 없으면
        return redirect(url_for("login.login_page"))

@bp.route('/ranking')
def ranking_page():
    return render_template('main/ranking_page.html')

@bp.route('/setting')
def setting_page():
    return render_template('main/setting_page.html')