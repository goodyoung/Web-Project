from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main_page():
    print(session)
    return render_template('main/main_page.html')

@bp.route('/ranking')
def ranking_page():
    return render_template('main/ranking_page.html')

@bp.route('/setting')
def setting_page():
    return render_template('main/setting_page.html')