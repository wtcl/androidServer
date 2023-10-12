import random
from Crypto.Cipher import AES

key = ''.join([chr(random.randint(0, 255)) for i in range(16)])
iv = ''.join([chr(random.randint(0, 255)) for j in range(16)])
pre = "comment1=cooking%20MCs;userdata="
pos = ";comment2=%20like%20a%20pound%20of%20bacon"


def xor(a, b):
    if len(a) > len(b):
        return ''.join([chr(ord(x) ^ ord(y)) for x, y in zip(a[:len(b)], b)])
    else:
        return ''.join([chr(ord(x) ^ ord(y)) for x, y in zip(a, b[:len(a)])])


def enc(m,key,iv):
    padding = chr(16 - len(m) % 16) * (16 - len(m) % 16)
    m = m + padding
    print(len(key),len(iv))
    c = AES.new(key.encode(), AES.MODE_CBC, iv.encode()).encrypt(m)
    return c, m


def flip(c, m, m1,key,iv):
    l = len(m1)
    d = len(pre)
    c1 = xor(m[d:d + l], (xor(m1, c[d:d + l])))
    new_c = c[:d] + c1 + c[d + l:]
    new_m = AES.new(key.encode(), AES.MODE_CBC, iv.encode()).decrypt(new_c)
    return new_m

m0 = pre + "A" * 32 + pos
c, m = enc(m0,key,iv)
m1 = ";admin=true;"
new_m = flip(c, m, m1,key,iv)
if ";admin=true;" in new_m:
    print("success")
    print(new_m)