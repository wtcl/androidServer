from Crypto.Cipher import AES
import base64
import binascii
from hashlib import sha1
import codecs

def JO(ka):    # 奇偶校验
    k=[]
    a=bin(int(ka,16))[2:]
    for i in range(0,len(a),8):
        if(a[i:i+7].count('1')%2==0):
           k.append(a[i:i+7]+'1')
        else:
           k.append(a[i:i+7]+'0')
    knew=hex(int(''.join(k),2))
    return knew[2:]

a=[7,3,1,7,3,1]
b=[1,1,1,1,1,6]
print (sum(a[i]*b[i] for i in range(6))%10)
#7 [1,1,1,1,1,6,7]

cipher='9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
ciphertext=base64.b64decode(cipher)

v ='12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4'
no=v[:10]
birth=v[13:20]
date=v[21:28]
mrz_inf=no+birth+date
print(mrz_inf)
#mrz_inf='12345678<811101821111167'

h_mrz=sha1(mrz_inf.encode()).hexdigest()
kseed=h_mrz[:32]
c='00000001'
d=kseed+c
hD=sha1(codecs.decode(d,'hex')).hexdigest()
print(hD)
#hD='EB8645D97FF725A998952AA381C5307909962536'

ka=hD[:16]
kb=hD[16:32]
k1=JO(ka)
k2=JO(kb)
key=k1+k2
print(key)
#key='ea8645d97ff725a898942aa280c43179'

m=AES.new(binascii.unhexlify(key),AES.MODE_CBC,binascii.unhexlify('0'*32))
print(m.decrypt(ciphertext))