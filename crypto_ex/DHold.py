import math
from Crypto.Util.number import getPrime


def multimod(a,k,n):    #快速幂取模
    ans=1
    while(k!=0):
        if k%2:         #奇数
            ans=(ans%n)*(a%n)%n
        a=(a%n)*(a%n)%n
        k=k//2          #整除2
    return ans
def yg(n):		# 这样默认求最小原根
    k=(n-1)//2
    for i in range(2,n-1):
        if multimod(i,k,n)!=1 and multimod(i,2,n)!=1:
            return i

def runFermatPow(a, b,m):  #大数模幂运算快速算法
    result = 1
    while (b > 0) :
        if ((b & 1) == 1):
            result = (result * a) % m
        a = (a * a) % m
        b =b//2
    return result
def findModReverse(a, m):  # 这个扩展欧几里得算法求模逆
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
# p=int(input("请输入模p（要求为素数）："))
# g=int(input("在输入该模的一个源根："))
def main():
    p = getPrime(1000)
    g=yg(p)
    print(multimod(g,p-1,p))
    print("素数是", p)
    print("最小原根是", g)
    a = int(input("请输入私钥："))
    k = int(input("选取一个随机整数："))
    #m = int(input("请输入明文"))
    m=getPrime(600)
    # c_1=pow(g,k)%p
    c_1 = runFermatPow(g, k, p)

    # c_2=(pow(pow(g,a),k)*m)%p
    c_2 = (runFermatPow(c_1, a, p) * m) % p
    print("密文c_1", c_1, "密文c_2", c_2)
    # print("密文c_1",c_1,"密文c_2",c_2)
    v = runFermatPow(c_1, a, p)
    v_1 = findModReverse(v, p)
    print("解密后的明文",(c_2 * v_1) % p)
    print((c_2 * v_1) % p==m)

if __name__ == '__main__':
    main()

