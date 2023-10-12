#coding:utf-8
import re
import base64
from functools import cmp_to_key
import string
from itertools import product

wenben=''
with open("6.txt","r",encoding='utf-8') as f:
    for i in f.readlines():
        wenben+=i.replace("\n",'')
wenben=base64.b64decode(wenben)
print(wenben)
print([wenben[i] for i in range(len(wenben))])
def cmp(a,b):
    return bool(a>b)-bool(a<b)

def hanm(a,b):
    n=0
    for i in range(len(a)):
        n += bin(a[i] ^ b[i]).count('1')
    return n

ans = [10000,10000]
for i in range(2,41):
    str1=[]
    str2=[]
    str3=[]
    str4=[]
    for j in range(0,i): str1.append(wenben[j])
    for j in range(i,2*i): str2.append(wenben[j])
    for j in range(2*i,3*i): str3.append(wenben[j])
    for j in range(3*i,4*i): str4.append(wenben[j])
    x1=float(hanm(str1,str2))/i
    x2=float(hanm(str2,str3))/i
    x3=float(hanm(str3,str4))/i
    x4=float(hanm(str1,str4))/i
    x5=float(hanm(str1,str3))/i
    x6=float(hanm(str2,str4))/i
    aa=(x1+x2+x3+x4+x5+x6)/6
    ans.append(aa)

ans_sort=sorted(ans)
ans_index=[ans.index(ans_sort[i]) for i in range(4)]
print(ans_index)
# 29,5,2,24
plaintext='''!"',.:;?- 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'''
pt=[]
for i in plaintext:
    pt.append(ord(i))
pt=pt+[10,9]
for keylength in range(2,41):
    block = []
    for i in range(keylength):
        k = 0
        t = []
        while i + keylength * k < 2876:
            t.append(wenben[i + keylength * k])
            k += 1
        block.append(t)

    ab = []
    for i in range(keylength):
        b = [i for i in range(256)]
        for j in range(256):
            for k in block[i]:
                if (j ^ k) not in pt:
                    b.remove(j)
                    break
        ab.append(b)
    print(keylength,ab)

for i in product([84], [101], [114], [109], [105], [110], [97], [116], [111], [114], [32], [88], [58], [32], [66], [114], [105], [110], [103], [32], [116], [104], [101], [32], [110], [111], [105], [115], [101]):
    key=list(i)
    outk=''
    for i in key:
        outk+=chr(i)
    print('key:', outk)
    plain=''
    for i in range(len(wenben)):
        plain+=chr(wenben[i]^(key[i%29]))
    with open('mb.txt','a',encoding='utf-8') as f:
        f.write(plain+'\n')
    print(plain)
