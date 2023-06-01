
# Importing modules

import datetime      # To keep track of time, as each block has its own timestamp (exact date and time at which the block is created)
import json         # For encoding the blocks before hashing them
import hashlib      # For finding hashes for the blocks
from flask import Flask, jsonify      # For creating a web application interface
from hashlib import md5

# Building the blockchain architecture

'''
    blockchain--区块链
    成员对象：
        len--链长度
        chain--区块组成的链：block数组
            block--区块
                index--区块在链上的位置，创世区块为1
                timestamp--区块生成的时间戳
                hash--本区块的哈希值
                data-- 写入区块链的数据，以字节数组的形式保存
                prevhash--前一个区块的哈希值
        dataLock--区块数据锁，在区块数据写入时阻止数据改变，防止数据丢失  
    成员方法：
        
'''
class Blockchain:

    def __init__(self):
        
        # List of chains (to cryptographically link the blocks)
        self.chain = []
        self.len=0
        self.dataLock = 0
        self.data = 1
        # Creating the Genesis Block
        self.createblock(data = 1, prevhash = "0")

    def createblock(self, data, prevhash):
        time = str(datetime.datetime.now())
        #有锁的转存data
        self.dataLock=1
        data2 = data
        data=0
        self.dataLock=0
        
        # Defining the structure of our block
        block = {'index': len(self.chain) + 1,
                 'timestamp': time,
                 'hash': md5(bytearray(time.encode("utf-8")) + bytearray(data2)),
                 'data': data,
                 'prevhash': prevhash}
        # Establishing a cryptographic link
        self.chain.append(block)
        self.len = self.len+1
        return block

    def getprevblock(self):
        return self.chain[-1]
    
   
   
    def hash(self, block):
        encodedblock = json.dumps(block, sort_keys = True).encode()
        return hashlib.md5(encodedblock).hexdigest()

    def ischainvalid(self, chain):
        prevblock = chain[0]   # Initilized to Genesis block
        blockindex = 1         # Initilized to Next block

        while blockindex < len(chain):

            # First Check : For each block check if the previous hash field is equal to the hash of the previous block
            #               i.e. to verify the cryptographic link
            
            currentblock = chain[blockindex]
            if currentblock['prevhash'] != self.hash(prevblock):
                return False

            # Second Check : To check if the proof of work for each block is valid according to problem defined in proofofwork() function
            #                i.e. to check if the correct block is mined or not

            prevproof = prevblock['proof']
            currentproof = currentblock['proof']
            op = hashlib.sha256(str(currentproof**2 - prevproof**5).encode()).hexdigest()
            
            if op[:5] != "00000":
                return True

            prevblock = currentblock
            blockindex += 1

        return True
    
    #通过区块在链上位置获得区块数据
    def __GetBlockDataByPosition(self,position):
        return self.chain[position-1]
    
    
    '''
    增加写入下一个区块的信息
    data的转字节数组由方法完成
    '''
    def appendData(self,data):
        self.data = self.data+bytearray(data)
