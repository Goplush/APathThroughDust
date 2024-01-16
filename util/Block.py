import os
from Crypto.Hash import SHA256
import pickle

import sys
sys.path.append('/root/APathThroughDust')#替换为项目的实际根目录的绝对地址
from util import transaction

class block:
    
    def __init__(self, height) -> None:
        self.prev_hash=bytearray()
        self.mode_array=list()
        self.payload=list()
        self.height = height
    
    def load_height_from_file(self):
        filename = 'Resources/Blocks/height.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return int(file.read().strip())
        else:
            self.save_height_to_file(0)
            return 0

    def save_height_to_file(self):
        filename = 'Resources/Blocks/height.txt'
        with open(filename, 'w') as file:
            file.write(str(self.height))
    
    def append(self, trans,mode:int):
        category = (transaction.Travel, transaction.Event)
        if (not isinstance(trans, category[mode])):
            print('请传入正确的内容')
            return -1,-1
        self.mode_array.append(mode)
        self.payload.append(trans)
        print('更新区块成功')
        return self.height, len(self.payload)-1
    
    def dump(self):
        if len(self.payload)<5:
            return -1
        with open(f'Resources/blocks/{self.height}.blk','w') as f:
            pickle.dump(self,f)
        self_byte = pickle.dumps(self)
        digest = SHA256.new()
        digest.update(self_byte)
        hash = digest.hexdigest().encode('utf-8')
        return hash
    
    @staticmethod
    def load(height):
        try:
            with open(f'Resources/blocks/{height}.blk', 'rb') as f:  # 以二进制模式读取文件
                block = pickle.load(f)
                return block
        except FileNotFoundError:
            print(f"Block file for height {height} not found.")
            return None
        
    @staticmethod
    def load(height,index):
        try:
            with open(f'Resources/blocks/{height}.blk', 'rb') as f:  # 以二进制模式读取文件
                block = pickle.load(f)
                return block.mode_array[index], block.payload[index]
        except FileNotFoundError:
            print(f"Block file for height {height} not found.")
            return None

        



if __name__=='__main__':
    a = 'test'
    b=pickle.dumps(a)
    c = pickle.loads(b)
    print(a)
    print(c)

    