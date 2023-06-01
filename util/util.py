import os

def __copy(src_path, target_path):
    file_list = os.listdir(src_path)  # 找出当前文件夹的路径都有何文件
    # print(file_list)
    # 变量列表
    for file in file_list:
        path_src = os.path.join(src_path, file)  # 将文件列表里的文件或者文件夹与原文件夹路径拼接
        # print(path_src)
        result = os.path.isdir(path_src)  # 判断当前文件是否为一个文件夹
        # print(result)
        if result:  # 如果是文件夹，进行递归调用
            path = os.path.join(target_path, file)  # 在目标文件夹里面，创建同名文件夹
            os.mkdir(path)
            copy(path_src, path)
        else:  # 如果不是文件夹，那就直接复制
            with open(path_src, 'rb') as rstream:  # 找到源文件路径，二进制只读打开
                continuer = rstream.read()  # 读取后放到容器里面
                path_target = os.path.join(target_path, file)  # 将文件列表里的文件或者文件夹与目标文件夹路径拼接
                with open(path_target, 'wb') as wstream:
                    wstream.write(continuer)  # 写入文件