from flask import Flask, render_template, request
import sys
sys.path.append("/root/projs/APathThroughDust")
from util.DBCommand import getDBConnection, getPubKey, get_user_real_name
from util.rsaSignVerify import verify_sign
import json
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        name = request.form.get('name')
        signature = request.form.get('signature')
        
        # 验签
        realname = get_user_real_name(nickname)
        key = getPubKey(nickname)
        if not verify_sign(nickname+realname,key):
            return "验证失败"
        # 进行其他操作

        return f"收到了你的信息：昵称 - {nickname}, 姓名 - {name}, 签名 - {signature}"

    # 如果是 GET 请求，渲染主界面模板
    return render_template('index.html')

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        amount = request.form.get('amount')
        sender_signature = request.form.get('sender_signature')
        receiver_signature = request.form.get('receiver_signature')
        
        # 创建交易字典
        transaction_data = {
            'nickname': nickname,
            'amount': amount,
            'sender_signature': sender_signature,
            'receiver_signature': receiver_signature
        }
        
        # 将交易字典保存到 JSON 文件中
        transaction_file = f"transaction_{nickname}.json"
        with open(transaction_file, 'w') as f:
            json.dump(transaction_data, f)
        
    # 读取服务器上的所有交易文件名
    transaction_files = []
    for file in os.listdir():
        if file.startswith('transaction_') and file.endswith('.json'):
            transaction_files.append(file)
    
    return render_template('transaction.html', transaction_files=transaction_files)


@app.route('/transaction/<filename>', methods=['GET', 'POST'])
def view_transaction(filename):
    transaction_data = {}
    with open(filename, 'r') as f:
        transaction_data = json.load(f)
    
    if request.method == 'POST':
        user_signature = request.form.get('signature')
        
        # 在这里添加签名验证的代码
        # 如果验证成功，将用户签名写入交易文件
        
        transaction_data['user_signature'] = user_signature
        
        with open(filename, 'w') as f:
            json.dump(transaction_data, f)
    
    return render_template('view_transaction.html', transaction_data=transaction_data)

if __name__ == '__main__':
    app.run()
