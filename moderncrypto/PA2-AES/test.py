# -*- coding: cp936
from oracle import *
import re

# b'aHR0cHM6Ly93d3cudHIweS53YW5nLzIwMTcvMTAvMDYvQ3J5cHRvMS8='

C = '9F0B13944841A832B2421B9EAF6D9836813EC9D944A5C8347A7CA69AA34D8DC0DF70E343C4000A2AE35874CE75E64C31'
div = len(C)/3
C = [C[:32],C[32:64],C[64:]]
print(div)
print(C)

Oracle_Connect()
M = []
IVALUE = []
for b in range(2):
    print('Block', b + 1)
    IV = C[b]
    Ivalue = []
    iv = '00000000000000000000000000000000'
    iv = [iv[2 * i:2 * i + 2] for i in range(int(len(iv) / 2))]
    padding = 1
    for l in range(16):
        print("TESTING IVALUE's last", l + 1, 'block')
        for ll in range(l):
            # print(ll,iv,Ivalue)
            iv[ll] = hex(int(Ivalue[ll], 16) ^ padding)[2:].zfill(2)  # 更新 iv
        for n in range(256):  # 遍历 0x00-0xFF
            iv[l] = hex(n)[2:].zfill(2)
            data = ''.join(iv[::-1]) + C[b + 1]

            ctext = [int(data[2 * i:2 * i + 2],16) for i in range(int(len(data) / 2))]
            rc = Oracle_Send(ctext, 2)
            if str(rc) == '49':  # Padding 正确时,返回49，不正确返回48, 记录 Ivalue, 结束爆破
                Ivalue += [hex(n ^ padding)[2:].zfill(2)]
                break
        print('-------', ''.join(iv[::-1]))
        print('-------', ''.join(Ivalue[::-1]))
        padding += 1
    Ivalue = ''.join(Ivalue[::-1])
    IVALUE += [Ivalue]
    # IV 与 Ivalue 异或求密文
    print(IV,Ivalue)
    m = re.findall('[0-9a-f]+', str(hex(int(IV, 16) ^ int(''.join(Ivalue), 16))))[1]
    mm=''
    for i in range(len(m)):
        if i%2==0:
            mm+=chr(int(m[i]+m[i+1],16))
    M += [mm]
    print('--- Detecting Block', b + 1, '-- Done!')
    print('---', 'The IValue' + str(b + 1), 'is:', Ivalue)
    print('---', 'The M' + str(b + 1), 'is:', mm)
    print('-' * 50)
print(''.join(M))
Oracle_Disconnect()