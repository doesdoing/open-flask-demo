from flask import Flask, session, redirect, url_for, escape, request, make_response, render_template, abort, send_from_directory
from flask_jsonpify import jsonify
from datetime import timedelta
import os
import time
import json
import sqlite3_plus
import _find
from random_plus import random_plus
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
        data_val = sqlite3_plus.sqlite3_plus(Path='./sql/user.db', Tab='user').find(cookies=cookies)
        data_info['login_user'] = data_val[0]['name']
        data_info['level'] = data_val[0]['level']
        data_info['personal_img'] = data_val[0]['personal_img'] if data_val[0]['personal_img'] else './image/bill.jpg'
        start = request.args.get('start') if request.args.get('start')else ''
        end = request.args.get('end') if request.args.get('end')else ''
        arr_what=['user','server','network','sql','system','upload']
        if what:
            if what in arr_what:
                if what=='user':
                    if data_info['level'] == 'admin':
                        data = sqlite3_plus.sqlite3_plus(Path='./sql/'+what+'.db', Tab=what).find()
                        data_info['len'] = len(data)
                    else:
                        data = data_val
                        data_info['len'] = len(data_val)
                else:
                    data = sqlite3_plus.sqlite3_plus(Path='./sql/'+what+'.db', Tab=what).find()
                    data_info['len'] = len(data)
        if start and end:
            _IP = request.args.get('ip')
            _LOCATION = request.args.get('location')
            _PROJECTS = request.args.get('projects')
            _NAME = request.args.get('name')
            _SYS_FILE = request.args.get('SFN')
            _USERNAME = request.args.get('username')
            _LEVEL = request.args.get('level')
            _ARR={'ip':_IP,'location':_LOCATION,'projects':_PROJECTS,'name':_NAME,'src_name':_SYS_FILE,'username':_USERNAME,'level':_LEVEL}
            e1=''
            if _IP or _LOCATION or _PROJECTS or _NAME or _SYS_FILE or _USERNAME or _LEVEL:
                print(_ARR)
                for x in _ARR:
                    if _ARR[x]:
                        e1 = _find.find(target=x ,start=start,end=end, data=data, value=_ARR[x])
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
        data_val = sqlite3_plus.sqlite3_plus(Path='./sql/user.db', Tab='user').find(cookies=cookies)
        if index == 'login':
            return app.send_static_file('html/login.html')
        if cookies:
            if data_val[0]['cookies'] == cookies:
                if index:
                    return app.send_static_file('html/'+index+'.html')
                else:
                    return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


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
                return redirect(url_for('index'))
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
            value = sqlite3_plus.sqlite3_plus(Path='./sql/user.db', Tab='user').find(username=name)
            if value != []:
                    if (name in value[0]['username'] and Pass in value[0]['password']):
                        create_cookies = random_plus().random_plus(Many=50)
                        sqlite3_plus.sqlite3_plus(Path='./sql/user.db', Tab='user').update(Data={'cookies': create_cookies, 'ip': ip}, username=name)
                        res = make_response(redirect('/index'))
                        res.set_cookie("key", create_cookies, max_age=60*60)
                        return res
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
        cookies = random_plus().random_plus(Many=50)
        sqlite3_plus.sqlite3_plus(
            Path='./sql/user.db', Tab='user').update(Data={'cookies': cookies}, ip=value[0]['ip'])
        res = make_response(redirect('/'))
        res.delete_cookie("key")
        return res
    else:
        return redirect('/')


@app.route('/post/<do>/<what>', methods=['POST'])
def fuc(do, what):
    post_data = json.loads(request.get_data())
    if do == 'add':
        sqlite3_plus.sqlite3_plus(Path='./sql/'+what+'.db', Tab=what).add(Data=post_data)
    elif do == 'del':
        sqlite3_plus.sqlite3_plus(Path='./sql/'+what+'.db', Tab=what).delete(ID=post_data['ID'])
    elif do == 'change':
        sqlite3_plus.sqlite3_plus(Path='./sql/'+what+'.db', Tab=what).update(Data=post_data, ID=post_data['ID'])
    return 'done'


@app.route('/download/<filename>')
def Download(filename):
    Path = './static/uploads'
    lists = os.listdir(Path)
    if request.method == "GET":
        for x in lists:
            if filename in x:
                if os.path.isfile(os.path.join(Path, x)):
                    data = sqlite3_plus.sqlite3_plus(Path='./sql/upload.db', Tab='upload').find(sys_name=filename)
                    return send_from_directory(Path, x, as_attachment=True, attachment_filename=data[0]['src_name']+'.'+data[0]['file_type'])


@app.route('/upload/file', methods=['POST'])
def upload():
    if request.method == 'POST':
        file_class = ['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG','xlsx', 'gif', 'GIF', 'doc', 'docx', 'ppt', 'pptx']
        f = request.files['file1']
        Path = './static/uploads'
        src_name = f.filename.rsplit('.', 1)[0]
        ext = f.filename.rsplit('.', 1)[1]
        if ext in file_class:
            unix_time = int(time.time())
            new_filename = random_plus().random_plus(EN='T')+str(unix_time)
            f.save(os.path.join(Path, new_filename+'.'+ext))
            T = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data = {'src_name': src_name, 'sys_name': new_filename,'upload_time': T, 'file_type': ext}
            sqlite3_plus.sqlite3_plus(Path='./sql/upload.db', Tab='upload').add(Data=data)
            return 'done'
        else:
            return 'error'
    else:
        return 'error'


if __name__ == "__main__":
    app.run(port=80, threaded=True, debug=True)
