from socket import socket


class chain_management_server:
    def __init__(self):
        # 用于存储客户端连接的数组
        self.client_sockets = []

        # 创建一个TCP / IP套接字并绑定服务器地址和端口
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5050)
        self.server_socket.bind(server_address)

        # 开始监听客户端连接
        self.server_socket.listen(50)
        print('服务器已启动，等待客户端连接...')



    def __listen_loop(self):
        while True:
            # 等待客户端连接
            new_client_socket, new_client_address = self.server_socket.accept()

            # 将新的客户端连接添加到数组中
            self.client_sockets.append(new_client_socket)

            print('客户端已连接:', new_client_address)

            # 向新加入的客户端发送欢迎消息
            new_client_socket.send()
            welcome_message = '欢迎加入服务器！'.encode("utf-8")
            new_client_socket.send(welcome_message)

            # 接收和发送数据
            while True:
                data = new_client_socket.recv(1024)
                if data:
                    # 处理接收到的数据
                    print('接收到来自客户端的消息:', data.decode())
                    # 将消息发送给其他客户端
                    for client in self.client_sockets:
                        if client != new_client_socket:
                            client.sendall(data)
                else:
                    # 客户端断开连接
                    print('客户端已断开连接:', new_client_address)
                    # 从数组中移除已断开连接的客户端
                    self.client_sockets.remove(new_client_socket)
                    # 关闭连接
                    new_client_socket.close()
                    break

        # 关闭服务器套接字
        server_socket.close()