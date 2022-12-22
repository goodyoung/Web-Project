from flask import Blueprint, render_template, redirect, url_for, request, session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import WebProject
from ..form import RegisterForm, LoginForm

bp = Blueprint('login', __name__, url_prefix='/login')
wp = WebProject.instance()
# 로그인
@bp.route('/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit(): 
        # 각 id랑 psw가 맞는지.
        userid = request.form['userid']
        userpw = request.form['userpw']

        is_exist = wp.send_query("SELECT EXISTS (SELECT id FROM user WHERE id = '{}') AS success".format(userid))

        if (is_exist[0]["success"]):
            is_correct = wp.send_query("SELECT CASE WHEN pwd = '{}' THEN TRUE ELSE FALSE END AS success FROM user WHERE id = '{}'".format(userpw, userid))
            #user_pwd = wp.send_query("SELECT pwd FROM user WHERE id = '{}'".format(userid))
            if (is_correct[0]["success"]):
                session['logged_in'] = True
                session['id'] = userid
                
                return redirect(url_for("main.main_page"))
            else:
                flash('비밀번호 틀림')
                return redirect(url_for("login.login_page"))
            
        else:
            print('여긴가요요요요')
            flash('존재하지 않는 아이디')
            return redirect(url_for("login.login_page"))
        
    else:
        session['logged_in'] = False
        return render_template('login/login_page.html', form = form)




# 회원 가입
@bp.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # real_name이 character name일 듯
        username= request.form['username']
        userid= request.form['userid']
        userpw= request.form['userpw']
        is_exist = wp.send_query("SELECT EXISTS (SELECT id FROM user WHERE id = '{}') AS success".format(userid))

        # 1. name이 같나 확인한다. (기존 db에서)
        if (is_exist[0]["success"]):
            # 2. 같으면 x 다시 돌아가게
            # 다시 돌아가게 짠다.
            flash('별명을 다시 입력하세요!','success')
            ###################### redirect 인가??????????????
            return render_template('login/register_page.html', form = form)
        else:
            # 3. 다르면 그냥 회원가입 하게?? 가 맞는듯?
            # + db에 추가 하고 '/' 라우트로 이동.
            wp.send_query("INSERT INTO user(id, pwd, name) VALUES ('{}', '{}', '{}')".format(userid, userpw, username), commit=True)
            return redirect(url_for("login.login_page"))
    else:
        return render_template('login/register_page.html', form = form)
    
# 로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for("login.login_page"))