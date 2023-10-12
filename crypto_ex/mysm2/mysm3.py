import binascii


IV=[int(i,16) for i in '7380166f 4914b2b9 172442d7 da8a0600 a96f30bc 163138aa e38dee4d b0fb0e4e'.split()]
T_j=[int('79cc4519',16)]*16+[int('7a879d8a',16)]*48

def sm3_rotl(x,n):   # 移位加和运算
    x0=(x<<n)&0xffffffff
    x1=((x>>(32-n))&0xffffffff)
    return x0|x1

def sm3_ff_j(x, y, z, j):  # 布尔函数
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        ret = (x & y) | (x & z) | (y & z)
    return ret

def sm3_gg_j(x, y, z, j):  # 布尔函数
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        ret = (x & y) | ((~ x) & z)
    return ret

def sm3_p_0(x):     # 置换函数
    return x ^ (sm3_rotl(x, 9 % 32)) ^ (sm3_rotl(x, 17 % 32))

def sm3_p_1(x):     # 置换函数
    return x ^ (sm3_rotl(x, 15 % 32)) ^ (sm3_rotl(x, 23 % 32))

def sm3_cf(v_i, b_i):   # cf分组加密
    w = []
    for i in range(16): # 将Bi分为16个部分
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + b_i[k]*weight
            weight = int(weight/0x100)
        w.append(data)
    for j in range(16, 68):  # W16-W67的计算
        w.append(0)
        w[j] = sm3_p_1(w[j-16] ^ w[j-9] ^ (sm3_rotl(w[j-3], 15 % 32))) ^ (sm3_rotl(w[j-13], 7 % 32)) ^ w[j-6]
    w_1 = []  # W'的计算
    for j in range(0, 64):
        w_1.append(0)
        w_1[j] = w[j] ^ w[j+4]

    a, b, c, d, e, f, g, h = v_i

    for j in range(0, 64):  # 64次迭代
        ss_1 = sm3_rotl(((sm3_rotl(a, 12 % 32)) +e +(sm3_rotl(T_j[j], j % 32))) & 0xffffffff, 7 % 32)
        ss_2 = ss_1 ^ (sm3_rotl(a, 12 % 32))
        tt_1 = (sm3_ff_j(a, b, c, j) + d + ss_2 + w_1[j]) & 0xffffffff
        tt_2 = (sm3_gg_j(e, f, g, j) + h + ss_1 + w[j]) & 0xffffffff
        d = c
        c = sm3_rotl(b, 9 % 32)
        b = a
        a = tt_1
        h = g
        g = sm3_rotl(f, 19 % 32)
        f = e
        e = sm3_p_0(tt_2)
        a, b, c, d, e, f, g, h = map(lambda x:x & 0xFFFFFFFF ,[a, b, c, d, e, f, g, h])
    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ v_i[i] for i in range(8)]

def sm3_hash(msg):
    len1 = len(msg)        # 消息长度
    reserve1 = len1 % 64   # 64比特
    msg.append(0x80)       # 加一个1和7个0
    reserve1 = reserve1 + 1
    range_end = 56
    if reserve1 > range_end:  # 防止长度为63
        range_end = range_end + 64
    for i in range(reserve1, range_end):  # 添加0串
        msg.append(0x00)
    bit_length = (len1) * 8  # 01串的长度
    bit_length_str = [bit_length % 0x100]
    for i in range(7): # 获取16进制的位数
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):   # 获取完整字符串
        msg.append(bit_length_str[7-i])
    group_count = round(len(msg) / 64)  # 获取迭代64字节次数
    B = []
    for i in range(0, group_count):  # 将每个64字节分组
        B.append(msg[i*64:(i+1)*64])
    V = []
    V.append(IV)
    for i in range(0, group_count): # 对每个组进行分组加密
        V.append(sm3_cf(V[i], B[i]))
    y = V[i+1]
    result = ""
    for i in y:  # 十进制转16进制
        result = '%s%08x' % (result, i)
    return result

def sm3_kdf(z, klen): # z为16进制表示的比特串（str），klen为密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt=int(klen/32)+1   # 取整,64字节的循环次数
    zin = [i for i in bytes.fromhex(z.decode('utf8'))]
    ha = ""
    for i in range(rcnt):
        msg = zin  + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        ha = ha + sm3_hash(msg)  # Hash(Z|ct)
        ct += 1
    return ha[0: klen * 2]  # K
