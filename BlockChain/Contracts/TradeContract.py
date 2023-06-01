import Trade
from Server import main
'''
确认交易：有两方签名
生成交易查找记录
消息准备上链
'''

def tradeCorrection(trade:Trade) -> bool:
    sendname=trade.Trade.getTradeSender()
    recvname=trade.Trade.getReceiver()
    t=trade.Trade.getTimestamp()
    amount=trade.Trade.getAmount()
    sigSend=trade.Trade.getSigSend()
    sigRecv=trade.Trade.getSigRecv()
    if not trade:
        return False
    if not sigRecv():
        return False
    if not sigSend():
        return False
    
    if(main.is_nickname_registered(sendname)):
        pkSend=main.getPubKey(sendname)
    if(main.is_nickname_registered(recvname)):
        pkRecv=main.getPubKey(recvname)
    
    data=str(sendname+recvname+t+amount).encode("utf-8")
    verSend=main.verify_signature(data,sigSend,pkSend)
    verRecv=main.verify_signature(data,sigRecv,pkRecv)
    res=verSend and verRecv
    return res


def tradeRecordGen(trade):
    sendname=trade.Trade.getTradeSender()
    recvname=trade.Trade.getReceiver()
    t=trade.Trade.getTimestamp()
    amount=trade.Trade.getAmount()
    sigSend=trade.Trade.getSigSend()
    sigRecv=trade.Trade.getSigRecv()
    if tradeCorrection(trade):
        data=sendname+'=='+recvname+'=='+t+'=='+amount+'=='+sigSend+'=='+sigRecv
        return bytearray(data)
    
