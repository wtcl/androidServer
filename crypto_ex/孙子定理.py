from functools import reduce
import math
from Crypto.Util.number import getPrime

def findModReverse(a, m):
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def shuru():
    # R = input("请按顺序输入余数（每个数间以空格间隔，结束按回车）：").split(' ')
    # M = input("请按顺序输入模数（每个数间以空格间隔，结束按回车）：").split(' ')
    # R = [int(r) for r in R]
    # M = [int(m) for m in M]
    R=[2,3,2]
    M=[3,5,7]
    """
    print("请按顺序输入余数和模数：")
    for i in range(3):
        R.append(int(input()))
    for i in range(3):
        M.append(int(input()))
        M.append(getPrime(2048))
    """
    """"
    with open("input.txt",'r',encoding='utf-8') as f:
        lines=f.readlines()
        print(len(lines))
        for line in range(len(lines)):
            if line<3:
                R.append(int(lines[line]))
            if line>=3:
                M.append(int(lines[line]))
    """
    print("R: ",R)
    print("M: ",M)
    panduan = 1
    for i in range(len(M) - 1):
        for j in range(i+1,len(M)):
            panduan = panduan * math.gcd(M[i], M[j])
    return R,M,panduan

"""
此注释部分用于产生测试用模数
R=[2,3,5,7,9]
M=[]
for i in range(5):
   M.append(getPrime(128))
   产生几个素数
print(M)
"""

def main():
    # panduan = 1
    # while panduan:
    R, M, panduan = shuru()
    if panduan == 1:
        length = len(R)
        Y = []
        summ = reduce(lambda x, y: x * y, M)
        # print(summ)   # 乘积
        for i in range(length):
            Y.append(summ // M[i])
        C = []
        for i in range(length):
            C.append(findModReverse(Y[i], M[i]))
        RYC = 0
        print("Y: ", Y)
        print("C: ", C)
        for i in range(length):
            RYC += R[i] * Y[i] * C[i]
        print("结果为：", RYC % summ)
        panduan = 0
    else:
        print("您输入的模值不是互素的，请重新输入")

if __name__=='__main__':
    main()