from flask import Blueprint, render_template, redirect, url_for, g, request, flash
from ..db import WebProject
from werkzeug.security import check_password_hash,generate_password_hash
from ..form import Trypwd, Enroll

bp = Blueprint('myinfo', __name__, url_prefix='/myinfo')
wp = WebProject.instance()


@bp.route('/')
def setting_page():
    data =g.user["user_id"]
    return render_template('myinfo/setting_page.html', data = data)

@bp.route('/passcheck', methods=['GET', 'POST'])
def password():
    form = Trypwd()
    data = g.user["user_id"]
    if request.method == 'POST' and form.validate_on_submit():
        userpw = request.form['userpw2']
        user_pwd = wp.send_query("SELECT pwd FROM user WHERE id = '{}'".format(g.user['user_id']))
        
        if check_password_hash(user_pwd[0]['pwd'],userpw):
            print('여기까지 왔다요')
            return redirect(url_for("myinfo.infomodify"))
        
        else:
            flash('비밀번호 틀림')
            return redirect(url_for("myinfo.password"))

    else:
        return render_template('myinfo/myinfo_passcheck.html', form=form, data = data)
    
@bp.route('/infomodify', methods=['GET', 'POST'])
def infomodify():
    if(request.method == 'POST'):
        params = request.get_json()
        if len(params['value']) == 0:
            flash('다시 입력해 주세요')
            return redirect(url_for("myinfo.infomodify"))
        else:
            if params['column'] == 'name':
                wp.send_query("UPDATE user SET {} = '{}' WHERE id='{}'".format(params['column'], params['value'], g.user['user_id']), commit=True)
            else:
                wp.send_query("UPDATE user SET {} = '{}' WHERE id='{}'".format(params['column'], generate_password_hash(params['value']), g.user['user_id']), commit=True)
            return redirect(url_for("myinfo.infomodify"))
    user_info = {}
    user = wp.send_query("select * from user where id='{}'".format(g.user['user_id']))
    user_info['user_name'] = user[0]['name']
    user_info['user_id'] = user[0]['id']
    user_info['user_pwd']= user[0]['pwd']
    return render_template('myinfo/myinfo_modify.html', user_info = user_info)





@bp.route('/notice', methods=['GET'])
def notice():
    notice_dict = {}
    notice = wp.send_query("SELECT * FROM notice_board ORDER BY date DESC")
    notice_dict['item'] = notice
    user = wp.send_query("select * from user where id = '{}'".format(g.user['user_id']))
    notice_dict['admin'] = user[0]['admin']
    return render_template('myinfo/myinfo_notice.html',notice = notice_dict)


@bp.route('/content/<int:content_id>', methods=['GET'])
def content(content_id):
    content_dict = {}
    
    notice = wp.send_query("SELECT * from notice_board ORDER BY date DESC")
    page_list = [i['id'] for i in notice]
    content_dict['page_list'] = page_list
    content_dict['page'] = content_id
    
    content = wp.send_query("SELECT * from notice_board where id ={}".format(content_id))
    content_dict['content'] = content[0]
    return render_template('myinfo/myinfo_notice_content.html',contented=content_dict)

# 게시글 등록
@bp.route('/enroll', methods=['GET', 'POST'])
def enroll():
    form = Enroll()
    if request.method == 'POST' and form.validate_on_submit():  
        title = request.form['title']
        content = request.form['content']
        print(title,content)
        wp.send_query("INSERT INTO notice_board(title, content) VALUES ('{}', '{}')".format(title,content), commit=True)
        
        return redirect(url_for("myinfo.notice"))
    
    else:
        return render_template('myinfo/myinfo_notice_enroll.html', form=form)
    
# 삭제
@bp.route('/delete/<int:content_id>', methods=['GET'])
def delete(content_id):
    wp.send_query("DELETE FROM notice_board WHERE id = {}".format(content_id), commit=True)
    return redirect(url_for("myinfo.notice"))


@bp.route('/modify/<int:content_id>', methods=['GET','POST'])
def modify(content_id):
    content = wp.send_query("SELECT * from notice_board where id ={}".format(content_id))
    print('modify의')
    before = [content[0]['title'],content[0]['content']]
    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['content']
        after = [title, contents]
        
        if before != after:
            wp.send_query("update notice_board set title='{}', content='{}' where id={};".format(title,contents,content_id), commit=True)
            
        return redirect(url_for("myinfo.notice"))
    else:
        return render_template('myinfo/myinfo_notice_modify.html',content=content[0])