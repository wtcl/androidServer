from random import choice


def xor(a,b):   # 异或算法
    res=[]
    for i in range(len(a)):
        res.append(a[i]^b[i])

def rotl(x,n):   # 移位加和运算
    x0=(x<<n)&0xffffffff
    x1=((x>>(32-n))&0xffffffff)
    return x0|x1

def get_unit32_be(key_data):
    return key_data[0]<<24 | key_data[1]<<16 | key_data[2]<<8 | key_data[3]

def put_unit32_be(n):  # 得到四个8位的数据
    return [((n>>24)&0xff), ((n>>16)&0xff), ((n>>8)&0xff), ((n)&0xff)]

def padding(data):   # 填充到16的整数倍长度
    return data + [(16 - len(data) % 16) for _ in range(16 - len(data) % 16)]

def unpadding(data):  # 解填充
    return data[:-data[-1]]

def list_to_bytes(data):  # 将列表内数字全部转化为字节型
    return b''.join([bytes((i,)) for i in data])

def bytes_to_list(data):  # 将字节型数据转为数字列表
    return list(data)

def random_hex(x): # 随机生成n位字符串
    return ''.join([choice('0123456789abcdef') for _ in range(x)])
