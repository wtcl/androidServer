import math
from functools import reduce

def judge(secretMsg, subKeys: list, t):
    # subKeys为从小到大排列好的数组
    # step 1 两两互素
    for i in range(len(subKeys) - 1):
        for j in range(i + 1, len(subKeys)):
            if math.gcd(subKeys[i], subKeys[j]) != 1:
                return False
    # step 2 N > secretMsg > M
    n=len(subKeys)
    N=reduce(lambda x,y:x*y,subKeys[:t])
    M=reduce(lambda x,y:x*y,subKeys[n-t+1:])
    if N > M and (secretMsg - N) * (secretMsg - M) < 0:
        return True
    else:
        return False

def findModReverse(a, m):  # 这个扩展欧几里得算法求模逆
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def produce_zkey(d,n,k):
    # 生成子密钥
    subKeys = []
    for i in range(n):
        subkey_d = d[i]
        subkey_k = k % d[i]
        subKeys.append([subkey_k, subkey_d])
    print('子密钥为：',subKeys)
    return subKeys

def recover(t,subKeys):
    R = [subKeys[i][0] for i in range(t)]  # 余数
    M = [subKeys[i][1] for i in range(t)]  # 模数
    length = len(R)
    Y = []
    summ = reduce(lambda x, y: x * y, M)
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

def main():
    t = int(input('请输入门限（t, n）以及秘密k：\nt = '))
    n = int(input('n = '))
    k = int(input('k = '))
    d_nums = input('请输入子密钥相关的元素d，个数为n个，以逗号分割如：1,2,3,4：').split(',')
    d = []
    # 格式检测
    try:
        assert len(d_nums) == n
        d=[int(i) for i in d_nums]
    except BaseException:
        print('请按格式输入')
        exit(0)
    print(f"t = {t}, n = {n}\nk = {k}")
    # 判断d是否满足要求
    d.sort()
    if not judge(k, d, t):
        print('子密钥相关的d不满足条件')
        exit(0)
    # 生成子密钥
    subKeys=produce_zkey(d,n,k)
    # 恢复秘密
    recover(t,subKeys)

if __name__ == '__main__':
    main()