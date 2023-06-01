import datetime

import pymysql
from Crypto.PublicKey import RSA


# 获取到数据库的连接
def getDBConnection():
    connection = pymysql.connect(
        host='localhost',
        user='DustAdmin',
        password='zud9@6tCgKCfzzMg',
        db='APathThroughTheDust',
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