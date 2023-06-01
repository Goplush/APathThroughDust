from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

def __rsaKeyPairGen():
    # 生成 RSA 私钥
    key = RSA.generate(2048)

    # 获取私钥（PEM 格式）
    private_key = key.export_key(format='PEM')

    # 获取公钥（PEM 格式）
    public_key = key.publickey().export_key(format='PEM')
    
    print("私钥长度为："+str(private_key.__len__()))
    print("公钥长度为："+str(public_key.__len__()))

    # 返回私钥和公钥的 PEM 编码
    return private_key, public_key


def sign_data(private_key_path, data_path, signature_path):
    # 读取私钥
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())

    # 读取待签名内容
    with open(data_path, 'rb') as f:
        data = f.read()

    # 创建签名对象
    signer = PKCS1_v1_5.new(private_key)
    # 计算待签名内容的哈希值
    digest = SHA256.new(data)

    # 进行签名
    signature = signer.sign(digest)

    # 返回签名的base64编码结果
    signature_hex =  signature.hex()
    
    print(signature_hex)
    return signature_hex

def test1():
    private_key, public_key = __rsaKeyPairGen()
    f = open('BlockChain/Client/AlicePkey', 'wb')
    f.write(private_key)
    f.close()
    #Try to read key from file
    f = open('BlockChain/Client/AlicePkey', 'rb')
    key = RSA.importKey(f.read())

def test2():
    sign_data("BlockChain/Client/AlicePkey","BlockChain/Client/AliceData","BlockChain/Client/AliceSig")


def func3():
    #Write key to file
    key = RSA.generate(4096)
    f = open('keyfile.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

    #Read key from file
    f = open('keyfile.pem', 'rb')
    key = RSA.importKey(f.read())
test1()
