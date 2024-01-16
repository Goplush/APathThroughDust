import datetime

from Crypto.Hash import SHA256
import pymysql
from Crypto.PublicKey import RSA
import json


def getDBConnection():
    # 读取外部的 JSON 文件
    with open('db_config.json', 'r') as file:
        config = json.load(file)

    # 从 JSON 文件中获取数据库连接信息
    host = config['host']
    user = config['user']
    password = config['password']
    db = config['db']

    # 建立数据库连接
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


#把用户账户注册到数据库
def RegUser2DB(nickName, userType, validTime, publicKeyPem):
    # 连接到MySQL数据库
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 插入用户的注册信息
            sql = "INSERT INTO ChainUser (nickname, rsa_public_key, registration_time, user_type, valid_time) VALUES (%s, %s, %s, %s, %s)"
            nickname = nickName
            registration_time = datetime.datetime.now().strftime("%Y-%m-%d")
            user_type = userType
            # 修改usertype和validTime，将validTime单位统一为天
            if userType == 'personal':
                user_type = 1
                valid_time = validTime
            else:
                user_type = 2
                valid_time = validTime * 365

            cursor.execute(sql, (nickname, publicKeyPem, registration_time, user_type, valid_time))
        # 提交事务
        connection.commit()
        print("用户注册信息已成功插入数据库！")
        return True
    except:
        print("")
        return False
    finally:
        # 关闭数据库连接
        connection.close()



# 由用户的昵称得到他的公钥
def getPubKey(nickname):
    # 连接到MySQL数据库
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 查询特定用户的公钥
            sql = "SELECT rsa_public_key FROM ChainUser WHERE nickname = %s"
            cursor.execute(sql, (nickname,))
            result = cursor.fetchone()

            if result is not None:
                public_key = result['rsa_public_key']
                #print(f"用户 '{nickname}' 的公钥：{public_key}")
                return RSA.import_key( public_key)
            else:
               #print(f"用户 '{nickname}' 不存在。")
                return None

    finally:
        # 关闭数据库连接
        connection.close()
        
def get_user_real_name(nickname):
    # 连接到MySQL数据库
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 执行SELECT语句查询用户实名信息
            sql = "SELECT * FROM UserRealName WHERE nickname = %s"
            cursor.execute(sql, (nickname,))
            result = cursor.fetchone()

            if result:
                # 输出用户实名信息
                rname = result['real_name']
            else:
                print("未找到与该昵称匹配的用户实名信息！")

    finally:
        # 关闭数据库连接
        connection.close()

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
def insert_user_real_name(nickname, real_name, signature):
    # 连接到MySQL数据库
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 插入用户实名信息
            sql = "INSERT INTO UserRealName (nickname, real_name, hash_value) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nickname, real_name, signature))

        # 提交事务
        connection.commit()
        print("用户实名信息已成功插入数据库！")

    finally:
        # 关闭数据库连接
        connection.close()


def insert_travel_data(creator, participant, dest, start_date, end_date,h,i):
    # 建立数据库连接
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 插入数据的 SQL 查询
            sql = "INSERT INTO travel (creator, participant, destination, start_date, end_date, blk_h, blk_i) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            # 执行插入操作
            cursor.execute(sql, (creator, participant, dest, start_date, end_date, h, i))
        # 提交事务
        connection.commit()
        print("数据插入成功！")
    except Exception as e:
        # 发生错误时回滚更改
        connection.rollback()
        print(f"插入行程时发生错误：{e}")
    finally:
        # 关闭数据库连接
        connection.close()

def check_real_name(nickname):
    # 建立数据库连接
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 构造 SQL 查询
            sql = "SELECT * FROM UserRealName WHERE nickname = %s"
            # 执行查询
            cursor.execute(sql, (nickname,))
            # 获取查询结果
            result = cursor.fetchone()
            # 检查是否找到对应昵称的实名信息
            if result:
                return True
            else:
                return False
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        # 关闭数据库连接
        connection.close()

def insert_necessaries_data(participant, start_time, end_time, required_participant, description, event_index):
    # 建立数据库连接
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 插入数据的 SQL 查询
            sql = "INSERT INTO Necessaries (participant, start_time, end_time, required_participant, description, event_index, event_h, event_i) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            # 执行插入操作
            cursor.execute(sql, (participant, start_time, end_time, required_participant, description, str(event_index), str(-1), str(-1)))
        # 提交事务
        connection.commit()
        print("数据插入成功！")
    except Exception as e:
        # 发生错误时回滚更改
        connection.rollback()
        print(f"插入必须事件时发生错误：{e}")
    finally:
        # 关闭数据库连接
        connection.close()

def get_user_travels(nickname):
    # 建立数据库连接
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 查询特定昵称的全部行程
            sql = "SELECT * FROM travel WHERE participant = %s"
            cursor.execute(sql, (nickname ))
            # 将查询结果打包为列表
            user_travels = cursor.fetchall()
            print(user_travels)
            return user_travels
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        # 关闭数据库连接
        connection.close()

def get_required_necessaries(participant, start_time, end_time):
    # 建立数据库连接
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 查询特定参与者、开始时间和结束时间范围内的必要事件
            sql = "SELECT * FROM Necessaries WHERE participant = %s AND start_time >= %s AND end_time <= %s"
            cursor.execute(sql, (participant, start_time, end_time))
            # 获取查询结果
            required_necessaries = cursor.fetchall()
            return required_necessaries
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        # 关闭数据库连接
        connection.close()

def update_event_receipt(participant, start_date, end_date, index, rcpt_h, rcpt_i):
    # 建立数据库连接
    connection = getDBConnection()

    try:
        with connection.cursor() as cursor:
            # 更新符合条件的行的 event_h 和 event_i 值
            sql = "UPDATE Necessaries SET event_h = %s, event_i = %s WHERE participant = %s AND start_time = %s AND end_time = %s AND event_index = %s"
            cursor.execute(sql, (rcpt_h, rcpt_i, participant, start_date, end_date, index))
        # 提交事务
        connection.commit()
        print("数据更新成功！")
    except Exception as e:
        # 发生错误时回滚更改
        connection.rollback()
        print(f"发生错误：{e}")
    finally:
        # 关闭数据库连接
        connection.close()