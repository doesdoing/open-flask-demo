from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, abort
from flask_jsonpify import jsonify
from random_cookies import random_cookies
from datetime import timedelta
import json
from api.sqlite3.showSQL import sql_show_tab
from api.sqlite3.updateSQL import sql_update_Data
from api.sqlite3.addSQL import sql_add_data
from api.sqlite3.delSQL import sql_del_data
import create_my_json
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
        data_key = []
        tmp_data = []
        data_info['data'] = []
        data = []
        cookies = request.cookies.get('key')
        data_val = sql_show_tab(Path='./sql/user.db', Tab='user', cookies=cookies, cols=['ID', 'username', 'password', 'name', 'level', 'personal_img'])
        data_info['login_user'] = data_val[0][3]
        data_info['level'] = data_val[0][4]
        data_info['personal_img'] = data_val[0][5] if data_val[0][5] else './image/bill.jpg'
        start = request.args.get('start') if request.args.get('start')else ''
        end = request.args.get('end') if request.args.get('end')else ''
        if what == 'user':
            data_key = ['ID', 'username', 'password','call_me', 'level', 'personal_img']
            if data_info['level'] == 'admin':
                data = sql_show_tab(Path='./sql/user.db', Tab='user')
                data_info['len'] = len(data)
            else:
                data = data_val
                data_info['len'] = len(data_val)
        elif what == 'server':
            data = sql_show_tab(Path='./sql/server.db', Tab=what)
            data_info['len'] = len(data)
            data_key = ['ID', 'location', 'projects', 'ip','login_name', 'login_password', 'remark', 'software', 'os', 'model']
        elif what == 'network':
            data = sql_show_tab(Path='./sql/network.db', Tab=what)
            data_info['len'] = len(data)
            data_key = ['ID', 'location', 'projects', 'ip','login_name', 'login_password', 'remark']
        elif what == 'sql':
            data = sql_show_tab(Path='./sql/sql.db', Tab=what)
            data_info['len'] = len(data)
            data_key = ['ID', 'location', 'projects', 'ip','login_name', 'login_password', 'remark', 'databases']
        elif what=='system':
            data = sql_show_tab(Path='./sql/system.db', Tab=what)
            data_info['len'] = len(data)
            data_key = ['ID', 'projects', 'ip','login_name', 'login_password', 'remark']     
        if start and end:
            _IP = request.args.get('ip')
            _LOCATION = request.args.get('location')
            _PROJECTS = request.args.get('projects')
            if _IP or _LOCATION or _PROJECTS:
                for x in data:
                    if str(x[1:4]).lower().find(_IP or _PROJECTS or _PROJECTS) >= 0:
                        tmp_data.append(x)
                        data_info['data'] = create_my_json.json(key=data_key, data=tmp_data[int(start):int(end)])
                        data_info['len'] =len(tmp_data)
            else:
                data_info['data'] = create_my_json.json(
                    key=data_key, data=data[int(start):int(end)])
        return jsonify(data_info)
   


@app.route('/<index>')
def index(index):
    req = json.dumps(request.args)
    if req == "{}":
        cookies = request.cookies.get('key')
        data_val = sql_show_tab(Path='./sql/user.db',
                                Tab='user', cookies=cookies, cols=['cookies'])
        if cookies:
            if data_val[0][0] == cookies:
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
        data_val = sql_show_tab(Path='./sql/user.db',
                                Tab='user', cookies=cookies, cols=['cookies'])
        if cookies == None or cookies == '':
            return redirect('/login')
        if data_val:
            if cookies == data_val[0][0]:
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
            value = sql_show_tab(Path='./sql/user.db', Tab='user',
                                 username=name, password=Pass, cols=['username', 'password'])
            if value != []:
                if (name in value[0]):
                    if (Pass in value[0]):
                        create_cookies = random_cookies(50)
                        sql_update_Data(Path='./sql/user.db', Tab='user',
                                        Data={'cookies': create_cookies, 'ip': ip}, username=name)
                        res = make_response(redirect('/index'))
                        res.set_cookie(
                            "key", create_cookies, max_age=60*60)
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
        value = sql_show_tab(path='./sql/user.db',
                             Tab='user', ip=ip, cols=['ip'])
        cookies = random_cookies(50)
        sql_update_Data(Path='./sql/Data.db', Tab='user',
                        Data={'cookies': cookies}, ip=value[0])
        res = make_response(redirect('/'))
        res.delete_cookie("key")
        return res
    else:
        return redirect('/')


@app.route('/post/<do>/<what>', methods=['POST'])
def fuc(do, what):
    post_data = json.loads(request.get_data())
    res = ""
    if do == 'add':
        res = sql_add_data(Path='./sql/'+what+'.db', Tab=what, Data=post_data)
    elif do == 'del':
        res = sql_del_data(Path='./sql/'+what+'.db', Tab=what, Data=post_data)
    elif do == 'change':
        res = sql_update_Data(Path='./sql/'+what+'.db',
                              Tab=what, Data=post_data, ID=post_data['ID'])
    if res == None:
        return 'done'


if __name__ == "__main__":
    app.run(port=80, threaded=True, debug=True)
