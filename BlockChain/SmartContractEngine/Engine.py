'''
智能合约引擎，用来运行智能合约
'''
#运行交易智能合约
from BlockChain.Contracts.TradeContract import *
from BlockChain.Contracts.CommentContract import *
from RegisterServer.blockchain import Blockchain
class Engine:

    def runTradeContract(trade):
        rec=tradeRecordGen(trade)
        Blockchain.appendData(rec)
        return
    #运行评论智能合约
    def runCommentContract(comment):
        flag=checkRecord(comment)
        addComment()
        return