
import random
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import sqlite3_plus
import random_plus

app = Flask(__name__)


@app.route('/download/<filename>')
def Download(filename):
    Path = './static/uploads'
    lists = os.listdir(Path)
    print(lists)
    if request.method == "GET":
        for x in lists:
            if filename in x:
                if os.path.isfile(os.path.join(Path, x)):
                    data = sqlite3_plus.sqlite3_plus(
                        Path='./sql/upload.db', Tab='upload').find(sys_name=filename)
                    print(data)
                    return send_from_directory(Path, x, as_attachment=True, attachment_filename=data[0]['src_name']+'.'+data[0]['file_type'])


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            file_class = ['txt', 'png', 'jpg', 'xls', 'JPG',
                          'PNG', 'xlsx', 'gif', 'GIF', 'doc', 'docx']
            f = request.files['file']
            Path = './static/uploads'
            fname = secure_filename(f.filename)
            src_name = f.filename.rsplit('.', 1)[0]
            print(src_name)
            ext = fname.rsplit('.', 1)[1]
            if ext in file_class:
                unix_time = int(time.time())
                new_filename = random_plus.random_name(12)+str(unix_time)+'.'+ext
                f.save(os.path.join(Path, new_filename))
                T = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                aa = {'src_name': src_name, 'sys_name': new_filename,
                      'upload_time': T, 'file_type': ext}
                sqlite3_plus.sqlite3_plus(
                    Path='./sql/upload.db', Tab='upload').add(Data=aa)
                return redirect(url_for('upload'))
            else:
                render_template('upload.html')
        except:
            render_template('upload.html')
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, port='80')
