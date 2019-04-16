
# coding:utf-8

import random
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import time
app = Flask(__name__)


def random_c(num):
    B = ""
    A = random.sample(
        'qwertyuiopasdfghjklzxcvbnm7894561230', int(num))
    for x in range(len(A)):
        B = B + A[x]
    return B


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':            
        try:
            file_class=['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF']
            f = request.files['file']
            Path = './static/uploads'
            fname=secure_filename(f.filename)
            ext = fname.rsplit('.',1)[1]  # 获取文件后缀
            if ext in file_class:
                pass
                unix_time = int(time.time())
                new_filename=str(unix_time)+'.'+ext  # 修改了上传的文件名
                f.save(os.path.join(Path,new_filename))  #保存文件到upload目录
                return redirect(url_for('upload'))
            else:
                render_template('upload.html')
        except:
            render_template('upload.html')
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, port='80')
