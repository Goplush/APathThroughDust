import pickle
import socket
from urllib import request
from util.rsaSignVerify import get_key, generate_sign


class Message:
    '''
    要求content为str
    '''

    def __init__(self, sender, receiver, message_type, content):
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.req_num = 0
        self.signature = 0
        self.content = content


class PBFTNode:
    def __init__(self, node_id, host, port, nickname, pri_key_file):
        self.node_id = node_id
        self.total_nodes = []
        self.nickname = nickname
        try:
            self.pri_key = get_key(pri_key_file)
        except Exception as e:
            print("invalid private key file")
            exit(-1)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = []  # 存储待处理的消息
        self.view = 0  # 当前视图号
        self.view_change_in_progress = False  # 是否正在进行视图转换
        self.view_change_votes = {}  # 存储视图转换的投票信息

    def start(self):
        # 从服务器获取活跃节点的IP
        active_nodes = self.get_active_nodes()

        # 创建与其他节点的连接
        for node in active_nodes:
            if node != self.node_id:
                try:
                    # 创建连接
                    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    node_socket.connect((node["ip"], node["port"]))
                    self.total_nodes.append(node_socket)
                    print(f"Connected to node {node['id']} at {node['ip']}:{node['port']}")
                except Exception as e:
                    print(f"Failed to connect to node {node['id']} at {node['ip']}:{node['port']}: {str(e)}")

    def get_active_nodes(self):
        # 从服务器获取活跃节点的IP
        response = request.get(self.server_address)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch active nodes from the server.")
            return []

    def send_message(self, message, destination):
        # 发送消息到目标节点
        # 可以使用网络通信库（如socket）发送消息
        pass

    def receive_message(self):
        # 遍历节点的连接并接收消息
        for node_socket in self.total_nodes:
            try:
                data = node_socket.recv(1024)  # 接收消息
                if data:
                    message = pickle.loads(data)
                    self.message_queue.append(message)  # 将消息放入处理队列
            except Exception as e:
                print(f"Failed to receive message from socket: {str(e)}")
        pass

    def process_messages(self):
        # 处理待处理的消息队列
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.process_message(message)

    def process_message(self, message):
        # 根据消息类型调用对应的处理方法
        message_type = message.message_type
        if message_type == "PREPREPARE":
            self.process_pre_prepare(message)
        elif message_type == "COMMIT":
            self.process_commit(message)
        elif message_type == "REPLY":
            self.process_reply(message)
        elif message_type == "VIEW_CHANGE":
            self.process_view_change(message)
        elif message_type == "NEW_VIEW":
            self.process_new_view(message)
        else:
            print(f"Unknown message type: {message_type}")

    def send_pre_prepare(self, sequence_number):
        # 发送PRE-PREPARE消息
        # 实现PRE-PREPARE消息的构造和发送逻辑
        pass

    def send_commit(self, sequence_number):
        # 发送COMMIT消息
        # 实现COMMIT消息的构造和发送逻辑
        pass

    def send_reply(self, request_id):
        # 发送REPLY消息
        # 实现REPLY消息的构造和发送逻辑
        pass

    def send_view_change(self, new_view):
        # 发送VIEW-CHANGE消息
        # 实现VIEW-CHANGE消息的构造和发送逻辑
        pass

    def send_new_view(self, new_view):
        # 发送NEW-VIEW消息
        # 实现NEW-VIEW消息的构造和发送逻辑
        pass

    def process_pre_prepare(self, message):
        # 处理PRE-PREPARE消息
        sender = message.sender
        content = message.content

        # 验证消息是否来自主节点
        if self.is_primary(sender):

            # 创建并签名PREPARE消息
            self.sign_message(message)

            # 广播PREPARE消息给其他成员
            self.broadcast_message(content)

    def process_prepare(self, message):
        # 处理PREPARE消息
        # 实现PREPARE消息的处理逻辑
        pass

    def process_commit(self, message):
        # 处理COMMIT消息
        # 实现COMMIT消息的处理逻辑
        pass

    def process_reply(self, message):
        # 处理REPLY消息
        # 实现REPLY消息的处理逻辑
        pass

    def process_view_change(self, message):
        # 处理VIEW-CHANGE消息
        # 实现VIEW-CHANGE消息的处理逻辑
        pass

    def process_new_view(self, message):
        # 处理NEW-VIEW消息
        # 实现NEW-VIEW消息的处理逻辑
        pass

    def process_request(self, request):
        # 处理客户端的请求
        # 实现客户端请求的处理逻辑
        pass

    def initiate_view_change(self):
        # 触发视图转换过程
        # 实现视图转换的触发逻辑
        pass

    def handle_view_change_votes(self):
        # 处理视图转换的投票结果
        # 实现视图转换投票结果的处理逻辑
        pass

    def is_primary(self, node_id):
        # 判断节点是否为主节点
        # 实现判断逻辑
        pass

    def broadcast_message(self, message):
        # 广播消息给其他成员
        # 实现广播消息的逻辑
        pass

    def sign_message(self, message):
        sig = generate_sign(message.content, self.pri_key)
        message.signature = sig
        return

    def main_loop(self):
        # 节点的主循环
        while True:
            self.receive_message()
            self.process_messages()


