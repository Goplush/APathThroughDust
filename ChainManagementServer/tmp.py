import socket

# 创建一个TCP/IP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口
server_address = ('localhost', 8888)
server_socket.bind(server_address)

# 开始监听客户端连接
server_socket.listen(5)

# 用于存储客户端连接的数组
client_sockets = []

print('服务器已启动，等待客户端连接...')

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()

    # 将新的客户端连接添加到数组中
    client_sockets.append(client_socket)

    print('客户端已连接:', client_address)

    # 向所有客户端发送欢迎消息
    welcome_message = '欢迎加入服务器！'
    for client in client_sockets:
        client.sendall(welcome_message.encode())

    # 接收和发送数据
    while True:
        data = client_socket.recv(1024)
        if data:
            # 处理接收到的数据
            print('接收到来自客户端的消息:', data.decode())
            # 将消息发送给其他客户端
            for client in client_sockets:
                if client != client_socket:
                    client.sendall(data)
        else:
            # 客户端断开连接
            print('客户端已断开连接:', client_address)
            # 从数组中移除已断开连接的客户端
            client_sockets.remove(client_socket)
            # 关闭连接
            client_socket.close()
            break

# 关闭服务器套接字
server_socket.close()
