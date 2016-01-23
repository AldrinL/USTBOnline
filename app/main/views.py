from datetime import datetime
from flask import render_template, session, redirect, current_app, url_for, request , make_response, flash, session
from . import main
from .forms import BindingForm
from .. import db
from ..models import db, User, School
from ..school import getOpener, USTB
from ..wxmsgr import wxinit, todict, toxml, getwxid
# import json
# import urllib.request
# from app.database import db_session

@main.before_app_first_request
def before_first_request(): 
    current_app.USTB=School('USTB')
    current_app.code=''


# @main.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()

@main.route('/' )
def hello_world():
    return 'Hello World!~'

@main.route('/wx', methods = ['GET', 'POST'] )
def init_auth():
    if request.method == 'GET':
        signature = request.args["signature"]
        timestamp = request.args["timestamp"]
        nonce = request.args["nonce"]
        echostr = request.args["echostr"]
        return wxinit(signature, timestamp, nonce, echostr)
    else:
        print(request.data)
        dict = todict(request.data)
        if dict['MsgType'] == 'event' and dict['Event'] == 'CLICK' and dict["EventKey"] == "cx":
            # url = 'http://ustbonline.coding.io' + url_for('main.grade', opid = dict['FromUserName'])
            url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3bd2eedb7bee8069&redirect_uri=http://ustbonline.coding.io'+ url_for('main.grade') +'&response_type=code&scope=snsapi_base#wechat_redirect' 
            return toxml(dict, url)


@main.route('/bd', methods = ['GET', 'POST'] )
def oauth():
    session['opid']=getwxid(request.args.get("code"))
#     return redirect(url_for('main.binding'))

# @main.route('/binding', methods = ['GET', 'POST'])
# def binding():
    state = None
    form = BindingForm()
    if session.get('opid'):
        print(session['opid'])
        opid=session['opid']
        print('session中有opid',session['opid'])
    else:
        opid=getwxid(request.args.get("code"))
        session['opid'] = opid
        print('通过函数获得opid', opid)
    if  opid and form.validate_on_submit():
        ustb=USTB(form.stuid.data, form.pswd.data)
        opener = ustb.login()
        if opener :
            user=User.query.filter_by(wxid=opid).first()
            if user:
                state='已重新绑定'
            else:
                user = User(opid, form.stuid.data, form.pswd.data, current_app.USTB)
                db.session.add(user)
                flash('恭喜:), 绑定成功!')
            state = '已绑定'
        else:
            flash('绑定失败:(, 请检查学号密码是否正确')
        form.stuid.data = ''
    else:
        state='请使用微信登录'
    return render_template('binding.html', form=form, state=state)


@main.route('/grade', methods = ['GET', 'POST'] )
def grade():
    if session.get('opid'):
        opid=session['opid']
    else:
        opid=getwxid(request.args.get("code"))
    print(opid)
    print('2',request.args.get("code"))
    user = User.query.filter_by(wxid=opid).first()
    if user:
        ustb=USTB(user.stuid, user.pswd)
        opener = ustb.login()
        grade=ustb.getgrade(opener)
        return render_template('grade.html', grade=grade, lenth = len(grade))
    else:
        flash('请先绑定')
        return render_template('404.html'), 404