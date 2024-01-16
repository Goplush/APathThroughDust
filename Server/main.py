from datetime import datetime
import threading
from flask import redirect, request, render_template, abort, send_from_directory
import flask  # For creating a web application interface
import sys
sys.path.append('/root/APathThroughDust')#替换为项目的实际根目录的绝对地址
from util.DBCommand import (
    RegUser2DB, getPubKey, insert_necessaries_data, is_nickname_registered, 
    insert_user_real_name, check_real_name, insert_travel_data,get_user_travels,
    get_required_necessaries, update_event_receipt
)
import os
import util.rsaSignVerify as rsautil
from util.transaction import Event, Necessary, Travel, TravelMapper
from util.rsaSignVerify import verify_sign
from util import TimestampGenerator, Block

block = Block.block(0)
block_lock = threading.Lock()

app = flask.Flask(__name__,static_folder='static',static_url_path='/static')
timestampgenerator = TimestampGenerator.TimestampGenerator()




def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

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
        if username.__len__() > 15:
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
    keypem, pubkeypem = rsautil.rsaKeyPairGen()
    username = request.form['username']
    usertype = request.form['usertype']
    duration = request.form['duration']
    if (not RegUser2DB(username, usertype, duration, pubkeypem)):
        return "注册出现错误"

    # 将私钥写入临时文件
    filePath = 'Resources/TmpKeys/' + username + 'privatekey.pom'  # 私钥临时文件的相对地址
    keyfile = open(filePath, 'wb')
    keyfile.write(keypem)
    keyfile.close()

    temp_url = '123.56.121.72:50000/tempkeys/' + username + 'privatekey.pom'
    return render_template("postRegister.html", privatekeyURL=temp_url)



'''
私钥下载页面
'''
@app.route('/tempkeys/<filename>', methods=['GET'])
def serve_temp_file(filename):
    # 临时目录
    #print('进入私钥下载流程')
    relativeFilePathtoProj = 'Resources/TmpKeys/' + filename
    abPath=os.path.abspath("/root/APathThroughDust")
    # 发送文件
    print(abPath)
    return send_from_directory(abPath+'/', relativeFilePathtoProj, as_attachment=True)


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
    print(f"签名为{sig}")

    #print(nickName)
    #print(realName)
    #print(idNum)


    #确认昵称已经注册
    if(not is_nickname_registered(nickName)):
        return "还未注册，请返回主界面注册"
    pubKey = getPubKey(nickName)
    if(rsautil.verify_sign(realName+"+"+idNum,sig,pubKey)):
        insert_user_real_name(nickName,realName, sig)
        return "注册成功"
    return "签名错误，请确认私钥无误后重新提交实名认证申请"

@app.route('/addtravel', methods=['GET'])
def show():
    return render_template('addTravel.html')

@app.route('/addtravel', methods=['POST'])
def submit():
    creator = request.form['creator']
    participants = request.form['participants']
    destination = request.form['destination']
    startdate = request.form['start_date']
    enddate = request.form['end_date']
    creator_sig = request.form['creator_sign']
    participant_sig = request.form['participant_sign']
    if not check_real_name(participants):
        return '请使用实名后的账号'
    
    if not (is_valid_date(startdate) and is_valid_date(enddate)):
        print('日期格式错误')
    signed_message = f'{participants}+{destination}+{startdate}+{enddate}'
    if not (verify_sign(signed_message,creator_sig, getPubKey(creator)) and verify_sign(signed_message,participant_sig, getPubKey(participants))):
        print('请检查签名')
    necessary_events = []
    
    necessary_count = int(request.form['necessary_count'])
    travel = Travel(destination,creator,participants)
    j=0
    for i in range(necessary_count):
        p2 = request.form[f'p2_{i}']
        if not (check_real_name(p2) and p2 != participants):
            print(f'您的第{j+1}个必须事件存在问题，请联系管理员解决')
        info = request.form[f'info_{i}']
        insert_necessaries_data(participants,startdate,enddate,p2,info,j)
        travel.add_necessary(Necessary(p2, info))
        j+=1
    
    with block_lock:
        global block
        if len(block.payload)==5:
            prev_hash = block.dump()
            height = block.height+1
            newblock = Block.block(prev_hash,height)
            newblock.save_height_to_file()
            block = newblock
        rcpt_h, rcpt_i = block.append(travel,0)
    
    
    insert_travel_data(creator,participants,destination,startdate,enddate,rcpt_h,rcpt_i)

    
    

    # You can perform further operations with the travel data here
    # For now, let's print the received data
    print(f'Creator: {creator}')
    print(f'Participants: {participants}')
    print(f'Destination: {destination}')
    print(f'start on {startdate}')
    print(f'end on {enddate}')
    for i, event in enumerate(necessary_events):
        print(f'Necessary Event {i + 1}:  p2={event.p2}, info={event.info}')

    # You might want to process this data further, save it to a database, etc.
    # For now, this just prints the received data

    return f'成功创建行程，请查收区块链收据: height: {rcpt_h}, index: {rcpt_i}'

@app.route('/searchtravel')
def showSearch():
    return render_template('searchTravel.html', travels=None, nickname=None)

@app.route('/search', methods=['GET'])
def search_travel():
    nickname = request.args.get('nickname')
    if not check_real_name(nickname):
        return '请输入实名认证过的账号昵称'
    travels = get_user_travels(nickname)
    matching_travels = [travel for travel in travels if travel['participant'] == nickname]
    return render_template('searchTravel.html', travels=matching_travels, nickname=nickname)


@app.route('/edittravel', methods=['GET'])
def edit_travel():
    participants = request.args.get('participants')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    travel_necessary_events = get_required_necessaries(participants,start_date,end_date)


    return render_template('travel_details.html', participants=participants, start_date=start_date, end_date=end_date, necessary_events=travel_necessary_events)


@app.route('/addevent', methods=['GET'])
def add_event():
    participants = request.args.get('participants')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    return render_template('addEvent.html', participants=participants, start_date=start_date, end_date=end_date)

@app.route('/submitevent', methods=['POST'])
def submit_event():
    participants = request.form.get('participants')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    p2 = request.form.get('p2')
    print(f'p2\'s len is {len(p2)}')
    info = request.form.get('info')
    p1sig = request.form.get('p1signature')
    p2sig = request.form.get('p2signature')

    signed_message = f'{participants}+{start_date}+{end_date}+{info}'
    if p2 is not '':
        if not (verify_sign(signed_message,p1sig, getPubKey(participants)) and verify_sign(signed_message,p2sig, getPubKey(p2))):
            return '签名错误'
    if not verify_sign(signed_message,p1sig, getPubKey(participants)):
        return '签名错误'
    
    rcpt_h=0
    rcpt_i=0
    

    # 在这里处理提交的事件数据
    # 可以将其存储到数据库中或者进行其他操作
    travelmapper = TravelMapper(participants,start_date,end_date)
    event = Event(participants,p2,travelmapper,False,-1,info)
    with block_lock:
        global block
        if len(block.payload)==5:
            prev_hash = block.dump()
            height = block.height+1
            newblock = Block.block(prev_hash,height)
            newblock.save_height_to_file()
            block = newblock
        rcpt_h, rcpt_i = block.append(event,1)
    

    # 打印收到的参数
    print(f"Participants: {participants}, Start Date: {start_date}, End Date: {end_date}")
    print(f"p2: {p2}, info: {info}")

    
    return f'Please save the chain receipt: height:{rcpt_h}, index:{rcpt_i}'

@app.route('/addnecessaryevent', methods=['GET'])
def add_necessary_event():
    participants = request.args.get('participants')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    p2 = request.args.get('required_participant')
    necessaryIndex = request.args.get('event_index')
    info = request.args.get('description')

    return render_template('addNecessity.html', participants=participants, start_date=start_date, end_date=end_date, required_participant = p2, event_index = necessaryIndex, description = info)


@app.route('/submitnecessity', methods=['POST'])
def submit_necessary_event():
    participants = request.form['participants']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    p2 = request.form['required_participant']
    event_index = request.form['event_index']
    description = request.form['description']
    p1sig = request.form['p1signature']
    p2sig = request.form['p2signature']

    message = f'{participants}+{event_index}+{start_date}+{end_date}'
    if not (verify_sign(message,p1sig, getPubKey(participants))):
        print(f'p1:{participants}, signature error')
        print(f'{p1sig}')
        print(f'message:{message}')
        return '签名错误'
    if not (verify_sign(message,p2sig, getPubKey(p2))):
        print(f'p2:{p2}, signature error')
        print(f'{p2sig}')
        print(f'message:{message}')
        return '签名错误'

    travelMapper = TravelMapper(participants,start_date,end_date)

    nece_event = Event(participants,p2,travelMapper,True,event_index,description)
    rcpt_h=0
    rcpt_i=0

    with block_lock:
        global block
        if len(block.payload)==5:
            prev_hash = block.dump()
            height = block.height+1
            newblock = Block.block(prev_hash,height)
            newblock.save_height_to_file()
            block = newblock
        rcpt_h, rcpt_i = block.append(nece_event,1)
    update_event_receipt(participants,start_date,end_date,event_index,rcpt_h,rcpt_i)

    return f'成功更新了序号为[{event_index}]的必须事件!'
    

    


# Running the Web App
app.run(host='0.0.0.0', port=50000)
