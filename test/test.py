
import random
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import json
import sqlite3_plus
from random_plus import random_plus
app = Flask(__name__)


@app.route('/download/<filename>')
def Download(filename):
    Path = './static/uploads'
    lists = os.listdir(Path)
    if request.method == "GET":
        for x in lists:
            if filename in x:
                if os.path.isfile(os.path.join(Path, x)):
                    data = sqlite3_plus.sqlite3_plus(
                        Path='./sql/upload.db', Tab='upload').find(sys_name=filename)
                    return send_from_directory(Path, x, as_attachment=True, attachment_filename=data[0]['src_name']+'.'+data[0]['file_type'])


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        a=request.files['file1']
        try:
            file_class = ['txt', 'png', 'jpg', 'xls', 'JPG',
                          'PNG', 'xlsx', 'gif', 'GIF', 'doc', 'docx']
            f = request.files['file1']
            Path = './static/uploads'
            fname = secure_filename(f.filename)
            src_name = f.filename.rsplit('.', 1)[0]
            ext = f.filename.rsplit('.', 1)[1]
            if ext in file_class:
                unix_time = int(time.time())
                new_filename = random_plus().random_plus(EN='T')+str(unix_time)
                f.save(os.path.join(Path, new_filename+'.'+ext))
                T = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                data = {'src_name': src_name, 'sys_name': new_filename,
                        'upload_time': T, 'file_type': ext}
                sqlite3_plus.sqlite3_plus(
                    Path='./sql/upload.db', Tab='upload').add(Data=data)
                return 'done'
            else:
              return 'error'  
        except:
            return 'error'
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, port='80')
