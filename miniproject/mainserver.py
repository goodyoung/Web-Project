from flask import Flask, url_for, request, session, redirect, app,render_template, escape
import module as mo

df = mo.first()
name_list = df['name'].to_dict()
id_dict = df['userid'].to_dict()
psw_list = df['psw'].to_list()

app = Flask(__name__)
app.secret_key = 'secretkeys'

@app.route('/', methods = ['GET','POST'])
def index():    
    print('adhadsfh')
    if request.method == 'POST': 
        # 각 id랑 psw가 맞는지.
        name= request.form['username']
        psw= request.form['password']

        if name in list(id_dict.values()) :
            num = [k for k, v in id_dict.items() if v == name][0]

            if (str(psw_list[num]) == str(psw)):
                session['logged_in'] = True
                session['username'] = int(df['id'].iloc[num])
                
                return render_template('test.html')
            else:
                return 'wowowow'
            
        else:
            return 'wowowowasgasgassaassagsagasgasgsaasgsagasg'
        
                #return redirect(url_for('home')) 
    else:
        session['logged_in'] = False
        print('sagasdg')
        print(session)
        return render_template('index.html')
            
            
            
@app.route('/sign', methods = ['GET','POST'])
def sign():
    if request.method == 'POST':
        # real_name이 character name일 듯
        real_name= request.form['realname']
        name= request.form['username']
        psw= request.form['password']
        # 1. name이 같나 확인한다. (기존 db에서)
        if name in list(id_dict.values()) :
            # 2. 같으면 x 다시 돌아가게
            # 다시 돌아가게 짠다.
            return render_template('signin.html')
        else:
            # 3. 다르면 그냥 회원가입 하게?? 가 맞는듯?
            # + db에 추가 하고 '/' 라우트로 이동.
            mo.insertuser(real_name,name,psw)
            return redirect(url_for("index"))
        
    else:
        return render_template('signin.html')

@app.route('/leaderboard', methods = ['GET','POST'])
def learderboards():
    dic = mo.leaderboard()
    if  "username" in session:
        print('나는 여겨 있습니당당당당당')
        print(session)
        
    return render_template('leaderboard.html', lead = dic)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)