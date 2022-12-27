from flask import Blueprint, render_template, redirect, url_for, session, g, request,jsonify, flash
from ..db import WebProject, exp_manager
from datetime import date
import json
import random

bp = Blueprint('main', __name__, url_prefix='/')
wp = WebProject.instance()
em = exp_manager.instance()

@bp.route('/', methods = ['GET', 'POST'])
def main_page():
    if(request.method=="POST"):
        params = request.get_json()
        if(params["func"]=="store"):
            today = date.today().isoformat()
            act = "todo_complete" if params["is_complete"] else "todo_write"

            send = {"can_exp" : False, "exp" : 0}

            is_exists = wp.send_query("SELECT EXISTS (SELECT * FROM todo WHERE user_id = '{}' AND nth = {} AND date = '{}') AS success".format(g.user["user_id"], params["nth"], today))
            print(act)
            if(is_exists[0]["success"]):
                wp.send_query("UPDATE todo SET content='{}', is_complete={} WHERE user_id = '{}' AND nth = {} and date = '{}'".format(params["content"], params["is_complete"], g.user["user_id"], params["nth"], today), commit=True)
                if(act=="todo_complete"):
                    print("성공 exp 얻기")
                    send["can_exp"] = em.gain_exp(g.user["user_id"], act)
                    if(send["can_exp"]):
                        send["exp"] = em.exp_dict[act]
            else:
                wp.send_query("INSERT INTO todo(user_id, is_complete, content, nth, date) VALUES ('{}', {}, '{}', {}, '{}')".format(g.user["user_id"], params["is_complete"], params["content"], params["nth"], today), commit=True)
                if(act=="todo_write"):
                    print("작성 exp 얻기")
                    send["can_exp"] = em.gain_exp(g.user["user_id"], act)
                    if(send["can_exp"]):
                        send["exp"] = em.exp_dict[act]

        
        
        elif(params["func"]=="get"):
            send = wp.send_query("""WITH test AS
                (
                    SELECT 0 AS nth
                    UNION ALL
                    SELECT 1 AS nth
                    UNION ALL
                    SELECT 2 AS nth
                    UNION ALL
                    SELECT 3 AS nth
                    UNION ALL
                    SELECT 4 AS nth
                )
                SELECT test.nth, IFNULL(todo.is_complete, -1) AS is_complete , IFNULL(todo.content, "") AS content FROM test LEFT JOIN todo ON test.nth = todo.nth AND todo.user_id = '{}' AND todo.date = '{}' ORDER BY nth;
                """.format(g.user["user_id"], params["date"]))
        
        return json.dumps(send)
    

    log = session.get('logged_in')
    if log:
        # 로그인 중이면
        em.daily_exist(g.user["user_id"])
        main_data = {}
        # args id 가 있을 때
        if request.args.get('id'):
           back_id = request.args.get('id', type=int)
           wp.send_query("update user set background_id={} where id='{}';".format(back_id,g.user["user_id"]), commit=True)
        # args snow 가 있을 때
        elif request.args.get('snow'):
           snow_id = request.args.get('snow', type=int)
           wp.send_query("update user set snow={} where id='{}';".format(snow_id,g.user["user_id"]), commit=True)
            
        back_snow = wp.send_query("SELECT background_id, snow FROM user WHERE id = '{}'".format(g.user["user_id"]))
        back_id = back_snow[0]['background_id']
        snow_id = back_snow[0]['snow']
        
        result = wp.send_query("SELECT user_Lv, user_Exp FROM user WHERE id = '{}'".format(g.user["user_id"]))
        main_data["lv"] = result[0]["user_Lv"]
        main_data["exp"] = result[0]["user_Exp"]

        main_data["imgview"] = random.randrange(1,3)

        main_data["max_exp"] = em.lvup_dict[main_data["lv"]]
        main_data['background_id'] = back_id
        main_data['snow_id'] = snow_id
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
    
    max_page = (len(ranking) - 1) // number + 1

    item = ranking[first_number:last_number]
    
    rank_dict['item'] = item
    rank_dict['max_page'] = list(range(1,max_page+1))
    rank_dict['page'] = page
    for j,i in enumerate(ranking):
        if g.user['user_id'] == i['id']:
            rank_dict['myinfo'] = j+1
            rank_dict['mypage'] = int((j //10) +1)
    
    if request.method == 'POST':
        params = request.get_json()

        for ret1,ret2 in enumerate(ranking):
            te = True
            if params['value'] == ret2['id']:
                te = False
                print(ret1)
                user_page = int((ret1 //10) +1)
                data = {'user_page': user_page}
                return jsonify(data)
        if te:
            flash('다시하세요')

            return redirect(url_for('main.ranking_page'))
            

    return render_template('main/ranking_page.html',user_rank = rank_dict)
