from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import sys
sys.path.append('/root/APathThroughDust')#替换为项目的实际根目录的绝对地址
from util.DBCommand import getPubKey


# 由pem文件包装出密钥（用于读取用户保存的私钥）
def get_key(path):
    with open(path) as f:
        pem_data = f.read()
        return RSA.importKey(pem_data)

# 生成2048位rsa密钥对
def rsaKeyPairGen():
    # 生成 RSA 私钥
    key = RSA.generate(2048)

    # 获取私钥（PEM 格式）
    private_key = key.export_key(format='PEM')

    # 获取公钥（PEM 格式）
    public_key = key.publickey().export_key(format='PEM')

    print("私钥长度为：" + str(private_key.__len__()))
    print("公钥长度为：" + str(public_key.__len__()))

    # 返回私钥和公钥的 PEM 编码
    return private_key, public_key


'''
获取签名
paras：
    unsigned_data:str
    pri_key:RSA.import_key(<PEM_DATA>)
'''

def open_key(path):
    with open(path, "r") as key_file:
        key = RSA.import_key(key_file.read())
    return key

def generate_sign(unsigned_data, pri_key):
    signer = PKCS1_v1_5.new(pri_key)
    digest = SHA256.new()
    digest.update(unsigned_data.encode("utf-8"))
    signed_data = signer.sign(digest)
    return b64encode(signed_data).decode("utf-8 ")


def verify_sign(unsigned_data, signature, pub_key):
    #从昵称得到公钥
    verifier = PKCS1_v1_5.new(pub_key)
    digest = SHA256.new()
    digest.update(unsigned_data.encode("utf-8"))
    return verifier.verify(digest, b64decode(signature))


if __name__ == '__main__':
    private_key = open_key('Resources/TmpKeys/test2privatekey.pom')
    pub_key = getPubKey('test2')
    sign = generate_sign('test1+0+2024-04-04+2024-05-12', private_key)
    verify = verify_sign('test1+0+2024-04-04+2024-05-12' ,sign, pub_key)
    print(sign)