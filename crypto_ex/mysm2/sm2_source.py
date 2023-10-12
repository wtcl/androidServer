import mysm3
from random import choice
# 选择素域，设置椭圆曲线参数（二元扩域上的话，需要计算多项式）
# https://www.jianshu.com/p/e41bc1eb1d81
# https://www.jianshu.com/p/8fbd8cd84e1e
# https://blog.csdn.net/conquerwave/article/details/10229899
# https://link.springer.com/article/10.1007/s10623-005-3299-y?utm_source=cnki&utm_medium=affiliate&utm_content=meta&utm_campaign=DDCN_1_GL01_metadata
# http://hyperelliptic.org/EFD/g1p/auto-shortw-jacobian.html   牛牛牛
# https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201701&filename=1016245975.nh&uniplatform=NZKPT&v=q_HoLP7KdgqM5UMkSOmrTrV2hODAo5LFzhYHp6l4kuDnLVv0A5LSAlsi5Z0EJns8
# https://zhuanlan.zhihu.com/p/87490028

default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}


class SM2(object):
    def __init__(self, private_key, public_key, ecc_table=default_ecc_table):
        self.private_key = private_key  # 私钥
        self.public_key = public_key    # 公钥
        self.para_len = len(ecc_table['n'])   # 字符串n的长度
        self.ecc_a3 = (int(ecc_table['a'], 16) + 3) % int(ecc_table['p'],16)
        self.ecc_table = ecc_table  # ecc的所有参数

    def _kg(self, k, Point):  # kP运算
        Point = '%s%s' % (Point, '1')
        mask_str = '8'
        for i in range(self.para_len - 1):
            mask_str += '0'
        mask = int(mask_str, 16)
        Temp = Point
        flag = False
        for n in range(self.para_len * 4):  # para_len*4表示二进制形式下的长度
            if (flag):
                Temp = self._double_point(Temp)  # 倍点运算
            if (k & mask) != 0:  # k和mask按位与，如果某位同为1，结果该位则为1
                if (flag):
                    Temp = self._add_point(Temp, Point)   # 两个不同的点进行运算
                else:
                    flag = True
                    Temp = Point
            k = k << 1
        return self._convert_jacb_to_nor(Temp)   # 将jacb坐标转为仿射坐标

    def _double_point(self, Point):  # 倍点
        l = len(Point)  # 点的字符串长度
        len_2 = 2 * self.para_len
        if l< self.para_len * 2:  # 如果输入的点的长度不够，直接返回None
            return None
        else:
            x1 = int(Point[0:self.para_len], 16)   # 取出Point前一部分转换为十进制
            y1 = int(Point[self.para_len:len_2], 16)  # 取出Point后一部分转换为十进制
            if l == len_2:  # 如果输入的是二倍长度，就将z1置为1
                z1 = 1
            else:          # 如果输入长度不止两个点长，就z1置为后面的部分
                z1 = int(Point[len_2:], 16)

            T6 = (z1 * z1) % int(self.ecc_table['p'], base=16)
            T2 = (y1 * y1) % int(self.ecc_table['p'], base=16)
            T3 = (x1 + T6) % int(self.ecc_table['p'], base=16)
            T4 = (x1 - T6) % int(self.ecc_table['p'], base=16)
            T1 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (y1 * z1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * 8) % int(self.ecc_table['p'], base=16)
            T5 = (x1 * T4) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * 3) % int(self.ecc_table['p'], base=16)
            T6 = (T6 * T6) % int(self.ecc_table['p'], base=16)
            T6 = (self.ecc_a3 * T6) % int(self.ecc_table['p'], base=16)
            T1 = (T1 + T6) % int(self.ecc_table['p'], base=16)
            z3 = (T3 + T3) % int(self.ecc_table['p'], base=16)
            T3 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            x3 = (T3 - T5) % int(self.ecc_table['p'], base=16)

            if (T5 % 2) == 1:
                T4 = (T5 + ((T5 + int(self.ecc_table['p'], base=16)) >> 1) - T3) % int(self.ecc_table['p'], base=16)
            else:
                T4 = (T5 + (T5 >> 1) - T3) % int(self.ecc_table['p'], base=16)

            T1 = (T1 * T4) % int(self.ecc_table['p'], base=16)
            y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)

            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (x3, y3, z3) # 将三个坐标转化为一个长的16进制字符串

    def _add_point(self, P1, P2):  # 点加函数，P2点为仿射坐标即z=1，P1为Jacobian加重射影坐标
        # 基本算法和上面的倍点运算相似，主要是加法部分不太一样
        len_2 = 2 * self.para_len
        l1 = len(P1)
        l2 = len(P2)
        if (l1 < len_2) or (l2 < len_2):
            return None
        else:
            # 取出(X1,Y1,Z1)
            X1 = int(P1[0:self.para_len], 16)
            Y1 = int(P1[self.para_len:len_2], 16)
            if (l1 == len_2):
                Z1 = 1
            else:
                Z1 = int(P1[len_2:], 16)
            x2 = int(P2[0:self.para_len], 16)
            y2 = int(P2[self.para_len:len_2], 16)

            T1 = (Z1 * Z1) % int(self.ecc_table['p'], base=16)
            T2 = (y2 * Z1) % int(self.ecc_table['p'], base=16)
            T3 = (x2 * T1) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T3 - X1) % int(self.ecc_table['p'], base=16)
            T3 = (T3 + X1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * T2) % int(self.ecc_table['p'], base=16)
            T1 = (T1 - Y1) % int(self.ecc_table['p'], base=16)
            Z3 = (Z1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T5 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T4 = (X1 * T4) % int(self.ecc_table['p'], base=16)
            X3 = (T5 - T3) % int(self.ecc_table['p'], base=16)
            T2 = (Y1 * T2) % int(self.ecc_table['p'], base=16)
            T3 = (T4 - X3) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T3) % int(self.ecc_table['p'], base=16)
            Y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)

            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (X3, Y3, Z3)

    def _convert_jacb_to_nor(self, Point): # Jacobian加重射影坐标转换成仿射坐标
        len_2 = 2 * self.para_len
        x = int(Point[0:self.para_len], 16) # 提取出x坐标
        y = int(Point[self.para_len:len_2], 16)  # 提取出y坐标
        z = int(Point[len_2:], 16)  # 提取出z坐标
        z_inv = pow(z, int(self.ecc_table['p'], base=16) - 2, int(self.ecc_table['p'], base=16)) # 计算z^(p-2)%p，就是z在模p的意义下的逆，相当于1/z
        z_invSquar = (z_inv * z_inv) % int(self.ecc_table['p'], base=16)  # 计算z_inv的平方
        z_invQube = (z_invSquar * z_inv) % int(self.ecc_table['p'], base=16) # 计算z_inv的立方
        x_new = (x * z_invSquar) % int(self.ecc_table['p'], base=16) # 计算x=x*z^2
        y_new = (y * z_invQube) % int(self.ecc_table['p'], base=16)  # 计算y=y*z^3
        z_new = (z * z_inv) % int(self.ecc_table['p'], base=16)      # 计算z=z*1/z=1
        if z_new == 1:   # 如果z=1,将x,y转换为仿射坐标
            form = '%%0%dx' % self.para_len
            form = form * 2
            return form % (x_new, y_new)
        else:         # 如果z！=1,返回None
            return None

    def encrypt(self, data):    # 加密函数，data消息(bytes)
        msg = data.hex() # 消息转化为16进制字符串
        print('message: ',msg)
        k = ''.join([choice('0123456789abcdef') for _ in range(self.para_len)])     # 随机生成倍点的k的值
        C1 = self._kg(int(k,16),self.ecc_table['g'])  # 计算C1=kG=（x1,y1）
        print('C1=kG:',C1)
        S = self._kg(int(k,16),self.public_key)      # PB即为公钥，所以（x2,y2）=k*PB
        x2 = S[0:self.para_len]                      # 得到x2
        y2 = S[self.para_len:2*self.para_len]        # 得到y2
        print('kPb=(x2,y2):',(x2,y2))
        ml = len(msg)                                 # 求消息的16进制长度
        t = mysm3.sm3_kdf(S.encode('utf8'), ml / 2)    # 求解消息的kdf
        print('t=kdf(x2||y2,klen):',t)
        if int(t,16)==0:                              # 如果返回为全0，则返回None
            return None
        else:                                         # 如果kdf操作后返回不为0，则
            form = '%%0%dx' % ml
            C2 = form % (int(msg, 16) ^ int(t, 16))   # 求C2=M^t
            print('C2:',C2)
            C3 = mysm3.sm3_hash([i for i in bytes.fromhex('%s%s%s' % (x2, msg, y2))])  # 求C3=Hash(x2||M||y2)
            print('C3: ',C3)
            return bytes.fromhex('%s%s%s' % (C1,C2,C3)) # 返回密文C=C1||C2||C3

    def decrypt(self, data):     # 解密函数，data密文（bytes）
        data = data.hex()          # 将数据转为hex形式
        len_2 = 2 * self.para_len  # len_2
        C1 = data[0:len_2]         # 取出C1
        C2 = data[len_2:-64]       # 取出C2
        C3 = data[-64:]            # 取出C3
        print('C1,C2,C3:',(C1,C2,C3))
        S = self._kg(int(self.private_key,16),C1)  # 计算S=hC1，h为公钥
        print('S: ' , S)
        x2 = S[0:self.para_len]   # 取出x2
        y2 = S[self.para_len:len_2]  # 取出y2
        print('X2,Y2',(x2,y2))
        cl = len(C2)               # 得到C2长度
        t = mysm3.sm3_kdf(S.encode('utf8'), cl / 2)  # 再次计算kdf(x2||y2,cl/2)
        print('t:',t)
        if int(t, 16) == 0:        # 如果t为全0比特串，返回None
            return None
        else:                      # 如果t不为全0比特串
            form = '%%0%dx' % cl
            M = form % (int(C2,16) ^ int(t,16)) # 计算M'=C2^t
            print("M' : ",M)
            u = mysm3.sm3_hash([i for i in bytes.fromhex('%s%s%s' % (x2, M, y2))])  # 计算u=Hash(x2||M'||y2)
            print('u:',u)
            # 判断解密出的明文是否正确
            if int(u,16)%int(self.ecc_table['p'],16)==int(C3,16)%int(self.ecc_table['p'],16):
                return bytes.fromhex(M) # 返回明文
            else:
                return None
