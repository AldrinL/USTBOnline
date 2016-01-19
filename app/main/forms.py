from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import Required

class BindingForm(Form): #WTF表单类
    stuid = IntegerField('学号', validators=[Required()])
    pswd = PasswordField('密码', validators=[Required()])
    submit = SubmitField('绑定')