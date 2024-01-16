

import requests
class TravelMapper:
    def __init__(self,participant:str, startdate:str, enddate:str) -> None:
        self.start_date = startdate
        self.end_date = enddate
        self.participant = participant
    
class Necessary:
    def __init__(self, p2:str, info:str) -> None:
        #两个参与者，但是其中一个必须为其所属的行程的参与者
        self.p2=p2
        self.info=info
        
        


class Event:
    def __init__(self, self_participant:str, other_participant:str, belong_to:TravelMapper, isnessary = False, necessary_index = -1, info = '') -> None:
        self.self_participant = self_participant
        self.blk_height = -1
        self.blk_index = -1
        self.other_participant = other_participant
        self.belong_to = belong_to#属于的旅行
        self.isnessary = isnessary#这个事件是某个行程的必须事件
        self.necessary_index = necessary_index
        self.info=info
        self.sig1=None
        self.sig2=None
    
    def set_timestamp(self,time:int):
        self.timestamp=time
        self.blk_height=int(time/60)
        self.blk_index=time%60

class Travel:
    def __init__(self, dest, creater:str, participant:str) -> None:
        self.dest = dest    #目的地
        self.necessaries = list()
        self.participant = participant
        self.creater = creater
        self.start_date = ''
        self.end_date = ''
    
    def add_necessary(self, nec:Necessary):
        if nec.p2.__len__() is 0:
            print("必须事件必须有双方")
            return False
        self.necessaries.append(nec)
    

    
    

def get_server_timestamp():
        response = requests.get('http://123.56.121.72:50003/get_timestamp')
        if response.status_code == 200:
            timestamp = response.json()['timestamp']
            return timestamp
        else:
            print("Failed to retrieve timestamp")
            return None
        


if __name__=='__main__':
    #测试
    print('test')
    timestamp = get_server_timestamp()
    print(f"Server timestamp: {timestamp}")

