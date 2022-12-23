from flask import Blueprint, render_template, redirect, url_for, g, request, flash
from ..db import WebProject
from werkzeug.security import check_password_hash
from ..form import Trypwd

bp = Blueprint('myinfo', __name__, url_prefix='/myinfo')
wp = WebProject.instance()


@bp.route('/')
def setting_page():
    return render_template('myinfo/setting_page.html')

@bp.route('/passcheck', methods=['GET', 'POST'])
def password():
    form = Trypwd()
    print('sadgasdg')
    if request.method == 'POST' and form.validate_on_submit():
        userpw = request.form['userpw2']
        user_pwd = wp.send_query("SELECT pwd FROM user WHERE id = '{}'".format(g.user['user_id']))
        
        if check_password_hash(user_pwd[0]['pwd'],userpw):
            
            return redirect(url_for("myinfo.main_page")) # 다른 페이지
        
        else:
            flash('비밀번호 틀림')
            return redirect(url_for("myinfo.password"))

    else:
        return render_template('myinfo/myinfo_passcheck.html', form=form, name = g.user['user_id'])
    
@bp.route('/notice', methods=['GET'])
def notice():
    notice_dict = {}
    #현재 페이지
    notice = wp.send_query("SELECT * from notice_board")
    item = notice
    notice_dict['item'] = item
    return render_template('myinfo/myinfo_notice.html',notice = notice_dict)


@bp.route('/content/<int:content_id>', methods=['GET'])
def content(content_id):
    
    content_dict = {}
    
    notice = wp.send_query("SELECT * from notice_board")
    max_page = len(notice)
    page = content_id
    print('asd')
    content_dict['max_page'] = max_page
    content_dict['page'] = page
    content = wp.send_query("SELECT * from notice_board where id ={}".format(content_id))
    content_dict['content'] = content[0]
    return render_template('myinfo/myinfo_notice_content.html',contented=content_dict)


