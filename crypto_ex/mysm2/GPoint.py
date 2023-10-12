import math
from random import randint

default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}

def findModReverse(a, m):    # 寻找模逆
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def get_lucas(x,y,k):       # lucas函数
    delta=x**2-4*y
    k=str(bin(k))[2:]
    U,V=1,x
    for i in range(1,len(k)):
        U,V=pow(U*V,1,int(default_ecc_table['p'],16)) , pow((V**2+delta*U*U)*findModReverse(2,int(default_ecc_table['p'],16)),1,int(default_ecc_table['p'],16))
        if k[i]=='1':
            U,V=pow(((x*U+V)*findModReverse(2,int(default_ecc_table['p'],16))),1,int(default_ecc_table['p'],16)),pow(((x*V+delta*U)*findModReverse(2,int(default_ecc_table['p'],16))),1,int(default_ecc_table['p'],16))
    return U,V

def get_sq(gg):            # 模素数平方根的求解
    if int(default_ecc_table['p'],16)%4 ==3:
        u=(int(default_ecc_table['p'],16)-3)//4
        y=pow(gg,u+1,int(default_ecc_table['p'],16))
        z=pow(y,2,int(default_ecc_table['p'],16))
        if z==gg:
            return y
        else:
            return None
    elif int(default_ecc_table['p'],16)%8 ==5:
        u=(int(default_ecc_table['p'],16)-5)//8
        z=pow(gg,2*u+1,int(default_ecc_table['p'],16))
        if z%int(default_ecc_table['p'],16)==1:
            y=pow(gg,u+1,int(default_ecc_table['p'],16))
            return y
        elif z%int(default_ecc_table['p'],16)==int(default_ecc_table['p'],16)-1:
            y=pow(pow(2*gg,1,int(default_ecc_table['p'],16))*pow(4*gg,u,int(default_ecc_table['p'],16)),1,int(default_ecc_table['p'],16))
            return y
        else:
            return None
    elif int(default_ecc_table['p'],16)%8 ==1:
        u=(int(default_ecc_table['p'],16)-1)//8
        Y=gg
        t=1
        while t:
            X = randint(1, int(default_ecc_table['p'], 16) - 1)
            U, V = get_lucas(X, Y, 4 * u + 1)
            if pow(V, 2, int(default_ecc_table['p'], 16)) == pow(4 * Y ,1, int(default_ecc_table['p'], 16)):
                t=0
                return pow((V*findModReverse(2,int(default_ecc_table['p'],16))) ,1, int(default_ecc_table['p'], 16))
            if U % int(default_ecc_table['p'], 16) != 1 and U % int(default_ecc_table['p'], 16) != (int(default_ecc_table['p'], 16) - 1):
                t=0
                return None

def get_gpoint():   # 基点生成函数
    t=1
    while t:
        x = randint(0, int(default_ecc_table['p'], 16) - 1)
        afa = pow((x**3 + int(default_ecc_table['a'], 16)*x + int(default_ecc_table['b'], 16)) ,1, int(default_ecc_table['p'],16))
        if afa == 0:
            t=0
            return hex(x)[2:]
        if get_sq(afa):
            t=0
            return hex(x)[2:]+hex(get_sq(afa))[2:]
default_ecc_table['g']=get_gpoint()
print(default_ecc_table)
if pow(int(default_ecc_table['g'][-64:],16),2,int(default_ecc_table['p'],16))==pow(int(default_ecc_table['g'][:64],16)**3+int(default_ecc_table['a'],16)*int(default_ecc_table['g'][:64],16)+int(default_ecc_table['b'],16),1,int(default_ecc_table['p'],16)):
    print(1)
else:
    print(0)
