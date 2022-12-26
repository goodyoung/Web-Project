from flask import Blueprint, render_template, redirect, url_for, session, g, request,jsonify, flash
from ..db import WebProject, exp_manager
from datetime import date
import json

bp = Blueprint('main', __name__, url_prefix='/')
wp = WebProject.instance()
em = exp_manager.instance()

@bp.route('/', methods = ['GET', 'POST'])
def main_page():
    if(request.method=="POST"):
        params = request.get_json()
        
        
        return 
    

    log = session.get('logged_in')
    if log:
        # 로그인 중이면
        em.daily_exist(g.user["user_id"])
        main_data = {}

        result = wp.send_query("SELECT user_Lv, user_Exp FROM user WHERE id = '{}'".format(g.user["user_id"]))
        main_data["lv"] = result[0]["user_Lv"]
        main_data["exp"] = result[0]["user_Exp"]

        main_data["max_exp"] = em.lvup_dict[main_data["lv"]]

        today = date.today().isoformat()
        main_data["mission"] = wp.send_query("SELECT quest_solve FROM daily WHERE user_id = '{}' AND date = '{}'".format(g.user["user_id"], today))[0]["quest_solve"]

        return render_template('main/main_page.html', main_data=main_data)
    else:
        # 로그인 정보가 없으면
        return redirect(url_for("login.login_page"))

        
@bp.route('/ranking', methods=['GET', 'POST'])
def ranking_page():
    rank_dict = {}
    number = 10
    #현재 페이지
    page = request.args.get('page', type=int, default=1)
    first_number = (page-1) *number
    last_number =  (page*number)
    ranking = wp.send_query("SELECT id, user_Lv, user_Exp FROM user ORDER BY user_Lv DESC,user_Exp DESC")
    if request.method == 'POST':
        params = request.get_json()

        for ret1,ret2 in enumerate(ranking):
            te = True
            print(te)
            print('tete')
            if params['value'] == ret2['id']:
                te = False
                print('tetetetet')
                user_page = int((ret1 //10) +1)
                data = {'user_page': user_page}
                return jsonify(data)
            
        if te:
            print('asf')
            flash('다시하세요')
            redirect(url_for('main.ranking_page'))
            
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
