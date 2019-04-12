from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, abort
from flask_jsonpify import jsonify
from random_cookies import random_cookies
from datetime import timedelta
import json
import create_my_json
import sqlite3_plus
import _find
app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=6)
app.jinja_env.variable_start_string = '%%'
app.jinja_env.variable_end_string = '%%'
@app.route("/api/<what>", methods=['GET'])
def api_message(what):
    req = json.dumps(request.args)
    new_dict = json.loads(req)
    if len(new_dict) < 5:
        data_info = {}
        data_info['data'] = []
        data = []
        cookies = request.cookies.get('key')
        data_val = sqlite3_plus.sqlite3_plus(
            Path='./sql/user.db', Tab='user').find(cookies=cookies)
        data_info['login_user'] = data_val[0]['name']
        data_info['level'] = data_val[0]['level']
        data_info['personal_img'] = data_val[0]['personal_img'] if data_val[0]['personal_img'] else './image/bill.jpg'
        start = request.args.get('start') if request.args.get('start')else ''
        end = request.args.get('end') if request.args.get('end')else ''
        if what == 'user':
            if data_info['level'] == 'admin':
                data = sqlite3_plus.sqlite3_plus(
                    Path='./sql/user.db', Tab=what).find()
                data_info['len'] = len(data)
            else:
                data = data_val
                data_info['len'] = len(data_val)
        elif what == 'server':
            data = sqlite3_plus.sqlite3_plus(
                Path='./sql/server.db', Tab=what).find()
            data_info['len'] = len(data)
        elif what == 'network':
            data = sqlite3_plus.sqlite3_plus(
                Path='./sql/network.db', Tab=what).find()
            data_info['len'] = len(data)
        elif what == 'sql':
            data = sqlite3_plus.sqlite3_plus(
                Path='./sql/sql.db', Tab=what).find()
            data_info['len'] = len(data)
        elif what == 'system':
            data = sqlite3_plus.sqlite3_plus(
                Path='./sql/system.db', Tab=what).find()
            data_info['len'] = len(data)
        if start and end:
            _IP = request.args.get('ip')
            _LOCATION = request.args.get('location')
            _PROJECTS = request.args.get('projects')
            if _IP:
                e1 = _find.find(target='ip', start=start,
                                end=end, data=data, value=_IP)
                data_info['data'] = e1['data']
                data_info['len'] = e1['len']
            elif _LOCATION:
                e1 = _find.find(target='location', start=start,
                                end=end, data=data, value=_LOCATION)
                data_info['data'] = e1['data']
                data_info['len'] = e1['len']
            elif _PROJECTS:
                e1 = _find.find(target='projects', start=start,
                                end=end, data=data, value=_PROJECTS)
                data_info['data'] = e1['data']
                data_info['len'] = e1['len']
            else:
                data_info['data'] = data[int(start):int(end)]
        return jsonify(data_info)

@app.route('/<index>')
def index(index):
    req = json.dumps(request.args)
    if req == "{}":
        cookies = request.cookies.get('key')
        data_val = sqlite3_plus.sqlite3_plus(
            Path='./sql/user.db', Tab='user').find(cookies=cookies)
        if cookies:
            if data_val[0]['cookies'] == cookies:
                if index == 'server':
                    return app.send_static_file('html/server.html')
                elif index == 'network':
                    return app.send_static_file('html/network.html')
                elif index == 'sql':
                    return app.send_static_file('html/sql.html')
                elif index == 'user':
                    return app.send_static_file('html/admin.html')
                elif index == 'index':
                    return app.send_static_file('html/index.html')
                elif index == 'system':
                    return app.send_static_file('html/system.html')
            else:
                return app.send_static_file('html/login.html')
        else:
            return app.send_static_file('html/login.html')
        if index == 'login':
            return app.send_static_file('html/login.html')

@app.route('/')
def user():
    req = json.dumps(request.args)
    if req == "{}":
        cookies = request.cookies.get('key')
        data_val = sqlite3_plus.sqlite3_plus(
            Path='./sql/user.db', Tab='user').find(cookies=cookies)
        if cookies == None or cookies == '':
            return redirect('/login')
        if data_val:
            if cookies == data_val[0]['cookies']:
                return app.send_static_file('html/index.html')
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/login/check', methods=['POST'])
def set_cookie():
    ip = request.remote_addr
    name = request.form['username']
    Pass = request.form['password']
    if request.method == 'POST':
        if name != '' and Pass != '':
            value = sqlite3_plus.sqlite3_plus(
                Path='./sql/user.db', Tab='user').find(username=name)
            if value != []:
                if (name in value[0]['username']):
                    if (Pass in value[0]['password']):
                        create_cookies = random_cookies(50)
                        sqlite3_plus.sqlite3_plus(Path='./sql/user.db', Tab='user').update(
                            Data={'cookies': create_cookies, 'ip': ip}, username=name)
                        res = make_response(redirect('/index'))
                        res.set_cookie("key", create_cookies, max_age=60*60)
                        return res
                    else:
                        return redirect('/')
                else:
                    return redirect('/')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route("/logout/check", methods=['GET'])
def delete_cookie():
    req = json.dumps(request.args)
    if req == "{}":
        ip = request.remote_addr
        value = sqlite3_plus.sqlite3_plus(
            Path='./sql/user.db', Tab='user').find(ip=ip)
        cookies = random_cookies(50)
        sqlite3_plus.sqlite3_plus(Path='./sql/user.db', Tab='user').update(Data={'cookies': cookies}, ip=value[0]['ip'])
        res = make_response(redirect('/'))
        res.delete_cookie("key")
        return res
    else:
        return redirect('/')

@app.route('/post/<do>/<what>', methods=['POST'])
def fuc(do, what):
    post_data = json.loads(request.get_data())
    if do == 'add':
        sqlite3_plus.sqlite3_plus(
            Path='./sql/'+what+'.db', Tab=what).add(Data=post_data)
    elif do == 'del':
        sqlite3_plus.sqlite3_plus(
            Path='./sql/'+what+'.db', Tab=what).delete(ID=post_data['ID'])
    elif do == 'change':
        sqlite3_plus.sqlite3_plus(
            Path='./sql/'+what+'.db', Tab=what).update(Data=post_data, ID=post_data['ID'])
    return 'done'

if __name__ == "__main__":
    app.run(port=80, threaded=True, debug=True)
