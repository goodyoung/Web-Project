from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired('이름은 필수입력 항목입니다.')])
    userid = StringField('별명', validators=[DataRequired('별명은 필수입력 항목입니다.')])
    userpw = PasswordField('비밀번호',  validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])

class LoginForm(FlaskForm):
    userid = StringField('별명', validators=[DataRequired('별명은 필수입력 항목입니다.')])
    userpw = PasswordField('비밀번호',  validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])
    
class Trypwd(FlaskForm):
    userpw2 = PasswordField('비밀번호',  validators=[DataRequired('비밀번호를 입력해라~')])
    
class Enroll(FlaskForm):
    title = StringField('제목',  validators=[DataRequired('제목 입력 필수')])
    content = TextAreaField('내용',  validators=[DataRequired('내용 입력 필수')])