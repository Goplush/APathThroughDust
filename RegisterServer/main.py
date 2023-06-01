from flask import jsonify, request, render_template, abort, send_from_directory
import flask  # For creating a web application interface
import pymysql
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode
import datetime
import tempfile

from RegisterServer.DBCommand import getDBConnection, RegUser2DB
from util.rsaSignVerify import getPubKey

app = flask.Flask(__name__)


# Welcome page
@app.route('/', methods=['GET'])
def welcome():
    return render_template("welcome.html")




# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        usertype = request.form['usertype']
        duration = request.form['duration']
        cost = 0
        '''
        print(f"Username: {username}")
        print(f"User Type: {usertype}")
        print(f"Duration: {duration}")
        '''
        if not username or not usertype or not duration:
            abort(400)  # 触发400错误，跳转到错误页面
        elif username.__len__() > 15:
            render_template("用户名过长，请重试")
            return render_template("register.heml")
        if usertype == 'personal':
            cost = int(duration)
        else:
            cost = int(duration) * 1000
        return render_template('ConfirmRegister.html', username=username, usertype=usertype, duration=duration,
                               cost=cost)
    return render_template('register.html')


'''
确定注册（缴费）只能跳转，不能直接访问
生成密钥对
向数据库写入用户信息
    昵称--VARCHAR(50)
    注册时间--date
    公钥--BINARY(1500)
    用户类型--INT
        1：个人用户
        2：企业用户
    有效时间--INT

提示用户下载私钥（privatekeyURL）
'''


@app.route('/confirmReg', methods=['POST'])
def confirm():
    keypem, pubkeypem = rsaKeyPairGen()
    username = request.form['username']
    usertype = request.form['usertype']
    duration = request.form['duration']
    if (not RegUser2DB(username, usertype, duration, pubkeypem)):
        return "注册出现错误"

    # 将私钥写入临时文件
    filePath = 'BlockChain/Server/tempkeys/' + username + 'privatekey.pom'  # 私钥临时文件的相对地址
    keyfile = open(filePath, 'wb')
    keyfile.write(keypem)
    keyfile.close()

    temp_url = '123.56.121.72:5000/tempkeys/' + username + 'privatekey.pom'
    return render_template("postRegister.html", privatekeyURL=temp_url)



'''
私钥下载页面
'''
@app.route('/tempkeys/<filename>', methods=['GET'])
def serve_temp_file(filename):
    # 临时目录
    #print('进入私钥下载流程')
    relativeFilePathtoProj = 'BlockChain/Server/tempkeys/' + filename

    # 发送文件
    return send_from_directory("/root/projs/APathThroughtheDust2/", relativeFilePathtoProj, as_attachment=True)


''''
实名认证页面
向保存实名信息的数据库写入信息
    昵称--VARCHAR(50),
    真实姓名 VARCHAR(50),
    真实姓名+身份证的SHA256哈希值 BINARY(32),

'''
@app.route('/RealNameAuth',methods=['GET', 'POST'])
def realNameAuthentication():
    if request.method=='GET':
        return render_template('realNameAuth.html')

    #从表单中提取信息
    print('收到实名认证POST请求')
    nickName = request.form['nickname']
    realName = request.form['real_name']
    idNum    = request.form['id_number']
    sig      = request.form['signature']

    #print(nickName)
    #print(realName)
    #print(idNum)


    #确认昵称已经注册
    if(not is_nickname_registered(nickName)):
        return "还未注册，请返回主界面注册"
    pubKey = getPubKey(nickName)
    if(verify_sign(realName+"+"+idNum,sig,pubKey)):
        __insert_user_real_name(nickName,realName,idNum)
        return "注册成功"
    return "签名错误，请确认私钥无误后重新提交实名认证申请"





# 生成2048位rsa密钥对
def rsaKeyPairGen():
    # 生成 RSA 私钥
    key = RSA.generate(2048)

    # 获取私钥（PEM 格式）
    private_key = key.export_key(format='PEM')

    # 获取公钥（PEM 格式）
    public_key = key.publickey().export_key(format='PEM')

    # print("私钥长度为："+private_key.__len__())
    # print("公钥长度为："+public_key.__len__())

    # 返回私钥和公钥的 PEM 编码
    return private_key, public_key





# RSA公钥验签
def verify_sign(unsigned_data, signature, pub_key):
    verifier = PKCS1_v1_5.new(pub_key)
    digest = SHA256.new()
    digest.update(unsigned_data.encode("utf-8"))
    return verifier.verify(digest, b64decode(signature))


# 确认昵称是否被注册
def is_nickname_registered(nickname):
    # 连接到MySQL数据库
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 查询昵称是否存在
            sql = "SELECT COUNT(*) as count FROM ChainUser WHERE nickname = %s"
            cursor.execute(sql, (nickname,))
            result = cursor.fetchone()

            count = result['count']
            if count > 0:
                return True
            else:
                return False

    finally:
        # 关闭数据库连接
        connection.close()


# 向实名信息数据库中新增行
def __insert_user_real_name(nickname, real_name, id_number):
    # 计算真实姓名和身份证号的SHA256哈希值
    h = SHA256.new()
    h.update(bytearray(real_name + id_number))
    hash_value = h.digest()

    # 连接到MySQL数据库
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 插入用户实名信息
            sql = "INSERT INTO UserRealName (nickname, real_name, hash_value) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nickname, real_name, hash_value))

        # 提交事务
        connection.commit()
        print("用户实名信息已成功插入数据库！")

    finally:
        # 关闭数据库连接
        connection.close()






# Running the Web App
app.run(host='0.0.0.0', port=5000)
