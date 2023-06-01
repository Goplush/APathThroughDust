
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384
from Crypto.Signature import pkcs1_15

from BlockChain.Client.rsaSignVerify import sign_data
'''
交易类
'''
class Trade:
    def __init__(self,sendaddr,recvaddr,timestamp,amount):
        self.sendaddr=sendaddr
        self.recvaddr=recvaddr
        self.timestamp=timestamp
        self.amount=amount
        self.data=str(self.sendaddr+self.recvaddr+self.timestamp+self.amount).encode("utf-8")
        self.__sigSend=self.__signature(self.sendaddr)
        self.__sigRecv=self.__signature(self.recvaddr)

    def __str__(self) -> str:
        return "A trade of "+self.amount+" has been created between "+self.sendaddr+" and "+self.recvaddr+" at "+self.timestamp
    #getter
    def getTradeSender(self):
        return self.sendaddr
    def getReceiver(self):
        return self.recvaddr
    def getTimestamp(self):
        return self.timestamp
    def getAmount(self):
        return self.amount
    def getSigSend(self):
        return self.__sigSend
    def getSigRecv(self):
        return self.__sigRecv
    #签名
    def __signature(self,addr):
        sig=sign_data(f"BlockChain/Client/{addr}Pkey","BlockChain/Client/{addr}Data","BlockChain/Client/{addr}Sig")
        return sig
    
# trade=Trade("127.0.0.1","127.0.0.1","13:00","30000")
# print(trade)