from flask import Blueprint, render_template, redirect, url_for, request, session
from ..db import WebProject

bp = Blueprint('login', __name__, url_prefix='/login')
wp = WebProject.instance()

@bp.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST': 
        # 각 id랑 psw가 맞는지.
        userid = request.form['userid']
        userpw = request.form['userpw']

        is_exist = wp.send_query("SELECT EXISTS (SELECT id FROM user WHERE id = '{}') AS success".format(userid))

        if (is_exist[0]["success"]):
            is_correct = wp.send_query("SELECT CASE WHEN pwd = '{}' THEN TRUE ELSE FALSE END AS success FROM user WHERE id = '{}'".format(userpw, userid))

            if (is_correct[0]["success"]):
                session['logged_in'] = True
                session['id'] = userid
                
                return render_template('main/main_page.html')
            else:
                return '비밀번호 틀림'
            
        else:
            return '존재하지 않는 아이디'
        
    else:
        session['logged_in'] = False
        print(session)
        return render_template('login/login_page.html')

@bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        # real_name이 character name일 듯
        username= request.form['username']
        userid= request.form['userid']
        userpw= request.form['userpw']

        is_exist = wp.send_query("SELECT EXISTS (SELECT id FROM user WHERE id = '{}') AS success".format(userid))

        # 1. name이 같나 확인한다. (기존 db에서)
        if (is_exist[0]["success"] or len(username)==0 or len(userid)==0 or len(userpw)==0):
            # 2. 같으면 x 다시 돌아가게
            # 다시 돌아가게 짠다.
            return render_template('login/register_page.html')
        else:
            # 3. 다르면 그냥 회원가입 하게?? 가 맞는듯?
            # + db에 추가 하고 '/' 라우트로 이동.
            wp.send_query("INSERT INTO user(id, pwd, name) VALUES ('{}', '{}', '{}')".format(userid, userpw, username), commit=True)
            return redirect(url_for("login.login_page"))
        
    else:
        return render_template('login/register_page.html')
