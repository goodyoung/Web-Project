from flask import Blueprint, render_template, redirect, url_for, session, g, request
from ..db import WebProject
bp = Blueprint('main', __name__, url_prefix='/')
wp = WebProject.instance()

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
    rank_dict = {}
    number = 10
    #현재 페이지
    page = request.args.get('page', type=int, default=1)
    first_number = (page-1) *number
    last_number =  (page*number)
    ranking = wp.send_query("SELECT id, user_Lv, user_Exp FROM user ORDER BY user_Lv DESC,user_Exp DESC")

    max_page = (len(ranking) - 1) // number + 1
    
    item = ranking[first_number:last_number]
    
    rank_dict['item'] = item
    rank_dict['max_page'] = list(range(1,max_page+1))
    rank_dict['page'] = page
    for j,i in enumerate(ranking):
        if g.user['user_id'] == i['id']:
            rank_dict['myinfo'] = j+1
            rank_dict['mypage'] = int((j //10) +1)     
    return render_template('main/ranking_page.html',user_rank = rank_dict)

@bp.route('/setting')
def setting_page():
    return render_template('main/setting_page.html')


## 순위: 내 순위 찾았어 건영아 들어봐 아자ㅏ자자자ㅏ

## 예시 1: 내 순위가 3이다       1페이지          3        |          2
## 예시 2: 내 순위가 10이다      1페이지          10        |          9
## 예시 3: 내 순위가 13이다      2페이지          13        |          2
## 예시 4: 내 순위가 25이다      3페이지          23        |          4
## 예시 5: 내 순위가 37이다      4페이지          37        |          6
## tot t:      myinfo.      mypage        myinfo.     |.    myinfo-((mypage-1) *10)) -1 
