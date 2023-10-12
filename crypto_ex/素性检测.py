import random
import time
import math
from Crypto.Util.number import getPrime

def fermat(m,kk):
    if kk>0:
        a = random.randint(2, m - 2)
        g = math.gcd(a, m)
        if g == 1 and runFermatPow(a,m-1,m) == 1:
            print('这是一个素数的概率为' + str(1 - 1 / (2 ** (k-kk))))
            fermat(m, kk-1)
        else:
            print("这是一个合数！")
    else:
        print('这是一个素数的概率为'+str(1-1/(2**k)))


def runFermatPow(a, b,m):
    result = 1
    while (b > 0) :
        if ((b & 1) == 1):
            result = (result * a) % m
        a = (a * a) % m
        b =b//2
    return result
# https://blog.csdn.net/u013445530/article/details/38641775
# runFermatPow摘自上文，此算法主要用于求解大数的模幂运算快速运算，解决了原来自带算法（a ** (m - 1) % m）较慢的问题


# def my_gcd(p,q):
#     if p<q:
#         p,q=q,p
#     if q==0:
#         return p
#     return my_gcd(p%q,q)
# 此处为我自己写的函数，经测验可知速度不如math库自带gcd函数,但是基本差别不大，可作为参考

# a=int(input("请输入一个需要判断是否为素数的整数："))
a=getPrime(1400)
# 所需大数的位数
print(len(str(bin(a))))
# 打印二进制形式下的字符串长度+2
k=int(input("请输入安全参数k："))

start=time.time()
# 记录开始运算时间
fermat(a,k)
# 正式运算
end=time.time()
# 记录结束运算时间
print("所需时间为：",end-start)
# 打印耗时