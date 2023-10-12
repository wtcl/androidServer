from Crypto.Util.number import getPrime,isPrime
from multiprocessing import Process,Value,Manager
import math
import random


def multimod(a,k,n):    #快速模指数算法
    ans=1
    while(k!=0):
        if k%2:         #奇数
            ans=(ans%n)*(a%n)%n
        a=(a%n)*(a%n)%n
        k=k//2          #整除2
    return ans

def yg(n):		# 随机选取原根
    k=(n-1)//2
    while 1:
        i=random.randint(2,n-2)
        if multimod(i,k,n)!=1 and multimod(i,2,n)!=1:
            return i

def findModReverse(a, m):  # 扩展欧几里得算法求模逆
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def get_strong_prime(n,larg):  #多进程中的子进程，查找强素数
    p = getPrime(500)
    while (not isPrime(2 * p + 1)):
        if(n.value!=0):
            return
        p = getPrime(500)
    n.value=1
    print(2*p+1,"是一个强素数")
    larg.append(2*p+1)
    print(larg)

def pro(n,larg):    # 多进程开启函数
    ps=[]
    for i in range(8):
        p=Process(target=get_strong_prime, args=(n,larg,))
        p.start()
        ps.append(p)
    for i in ps:
        i.join()

def main():    # 主函数
    n = Value('l', 0)
    large_prm=Manager().list()
    pro(n,large_prm)
    p=large_prm[0]
    g=yg(p)
    print("强素数p:", p)
    print("随机原根g:", g)
    a=random.randint((p-1)//2,(p+(p-1)//2))
    k=random.randint(1,p-2)
    print('私钥a:',a)
    print('k:',k)
    #m = int(input("请输入明文"))
    m=random.randint(2**124+1,2**125)
    c_1 = multimod(g, k, p)
    c_2 = (multimod(c_1, a, p) * m) % p
    print("密文c_1:", c_1)
    print("密文c_2:", c_2)
    v = multimod(c_1, a, p)
    v_1 = findModReverse(v, p)
    print("解密后的明文m:",(c_2 * v_1) % p)
    if (c_2 * v_1) % p==m:
        print('解密正确！')
    else:
        print('解密错误')

if __name__ == '__main__':
    main()

