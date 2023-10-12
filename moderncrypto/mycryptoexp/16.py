from Crypto.Cipher import AES
import base64
import random

def addpadd(stri,length):
    psize=length-len(stri)
    psize=[psize]*psize
    #print(psize)
    psize=bytes(psize)
   # print(type(stri))
    return bytes(stri,encoding="utf-8")+psize
def addpaddaes(stri):
    length=(len(stri)//16+1)*16
    psize = length - len(stri)
    psize = [psize] * psize
    # print(psize)
    psize = bytes(psize)
    # print(type(stri))
    return bytes(stri,encoding="utf-8") + psize
def removepadd(stri):
    return stri[:len(stri)-stri[-1]]
# 加密方法
def encrypt_oracle(key,text):
    # 秘钥
    #print(key,type(key))
    # 待加密文本
    # 初始化加密器
   # key=bytes(key,encoding="utf-8")
    aes = AES.new(key, AES.MODE_ECB)
    # 先进行aes加密
   # print(text,type(text))
   # print(len(text))\
   # print(type(text))
    encrypt_aes = aes.encrypt(text)
    # print(type(encrypt_aes))
    # print(encrypt_aes)
    # 用base64转成字符串形式
    encrypted_text = str(encrypt_aes, encoding='utf-8',errors='ignore')  # 执行加密并转码返回bytes
    #print(type(encrypted_text))
    return encrypt_aes
# 解密方法
def decrypt_oralce(key,text):
    # 秘钥

    # 密文
    # 初始化加密器
   # print(key,type(key))
    aes = AES.new(key, AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    #base64_decrypted = text.encode(encoding='utf-8')
    # 执行解密密并转码返回str
    decrypted_aes=aes.decrypt(text)
    decrypted_text = str(decrypted_aes, encoding='utf-8',errors="ignore").replace('\0', '')
   # print('decrypted_text', decrypted_text)
    return decrypted_aes


# s="crytvuybijn"
# s=addpadd(s,20)
# print(s)
# print(removepadd(s))
def cbc_encrypt(key,iv,string):
    parm=(len(string)//16+1)*16
    string=addpadd(string,parm)
    cipertext=b""
    for i in range(parm//16):
        block=string[i*16:(i+1)*16]
       # print(len(block),len(iv))
        xorblock=[(a^b) for (a,b) in zip(block,iv)]
        #print(xorblock)
        #xorblock = b"".join(xorblock).encode()
        #print(type(xorblock))
        xorblock=bytes(xorblock)
        # print(xorblock)
        # print(len(xorblock))
        encryblock=encrypt_oracle(key,xorblock)


        cipertext+=encryblock
    return cipertext
def cbc_decrypt(key,iv,string):
    plaintext=""
    print(len(string))
    for i in range(len(string)//16):
        block=decrypt_oralce(key,string[i*16:i*16+16])
        decrypt_block=[chr(a^b) for (a,b) in zip(block,iv)]
        decrypt_block="".join(decrypt_block)
        plaintext+=decrypt_block
        iv=string[i*16:(i+1)*16]
    return plaintext
def generate_randomdata(length):
    data=[]
    for i in range(length):
        data.append(random.randint(0,255))
    return data
def random_encrypt(key,iv,string):
    flag=random.randint(0,1)
    randomFront=bytes(generate_randomdata(random.randint(5,10)))
    randomback=bytes(generate_randomdata(random.randint(5,10)))
    padding=addpaddaes(randomFront+string+randomback)
    #print(len(padding)%16)
    print(flag)

    if flag==1:
        ciphertext=encrypt_oracle(key,padding)
    else:
        ciphertext=cbc_encrypt(key,iv,padding)
    return ciphertext
def detect_mode(ciphertext):
    blocks=[ciphertext[b*16:16*(b+1)] for b in range(0,len(ciphertext)//16)]
    detect=[]
    print(blocks)
    for b in blocks:
        if blocks.count(b)>1:
            detect.append(b)
            print(b,blocks.count(b))
    if detect:
        print(detect)
        print("ECB MODE detected!")
# s=b"ertrytuytyrgerfsdasWDEFWRTY6U76KILOUIYUJTHRGEFWDQDEWRET6U5768IYUJTNYBTRVFEDWSQDFGRTHYJM"
# key=b"aegrthyutyrthr23"
"""challange9,10
iv=[0]*16
# print(type(s))
# print(cbc_encrypt(key,iv,s))
# sb=cbc_encrypt(key,iv,s)
# print(len(sb))
# ss=cbc_decrypt(key,iv,sb)
# print(ss)
f=open('cipher.txt','r')
s=f.read()
ciphertext=base64.b64decode(s)
#print(ciphertext.decode(encoding="utf-8",errors="ignore"))
key=b"YELLOW SUBMARINE"
plaintext=cbc_decrypt(key,iv,ciphertext)
plaintext=removepadd(plaintext.encode())
print(plaintext.decode())
#print(bytes(plaintext))
#print(cbc_encrypt())
"""
"""
#chanllage11
key=bytes(generate_randomdata(16))
print(key)
iv=generate_randomdata(16)
string=b"I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight; and the glory of the Lord shall be revealed and all flesh shall see it together." * 10

ciphertext=random_encrypt(key,iv,string)
detect_mode(ciphertext)

"""
"""
#chanllage 14
unkownstring=base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
key=bytes(generate_randomdata(16))
randomPrefix=bytes(generate_randomdata(random.randint(2,32)))
def encrypt(string):
    plaintext=randomPrefix+bytes(string)+unkownstring
    cipertext=encrypt_oracle(key,addpaddaes(plaintext))
    return cipertext
def detect_blocksize():
    ruplien=len(encrypt([]))
    p1=p2=b''
    l1=l2=ruplien
    while l1==l2:
        p1+=b'A'
        l2=len(encrypt(p1))
    l1=l2
    while l1==l2:
        p2+=b'A'
        l2=len(encrypt(p1+p2))
    paddinglen=len(p1)-1
    blocksize=len(p2)
    rulen=ruplien-paddinglen
    buf=[0x41]*blocksize*2
    flag=False
    while not flag and len(buf)<blocksize*3:
        ciphertext=encrypt(buf)
        ctblock=[ciphertext[c*blocksize:blocksize*(c+1)] for c in range(len(ciphertext)//blocksize)]
        for i in range(len(ctblock)-1):
            if ctblock[i]==ctblock[i+1]:
                flag=True
            if not flag:
                buf+=[0x41]
    rpadlen=len(buf)-blocksize*2
    offset=0
    buf=[0x41]*blocksize*3
    ciphertext=encrypt(buf)
    cblock=[ciphertext[c*blocksize:blocksize*(c+1)] for c in range(len(ciphertext)//blocksize)]
    for i in range(len(cblock)-1):
        if cblock[i]==cblock[i+1]:
            offset=i
            break
    randoprefixlen=offset*blocksize-rpadlen
    return (randoprefixlen,ruplien-paddinglen-randoprefixlen,blocksize)
def generate_cipherexts(buffer):
    buffers={}
    for b in range(256):
        buffers[b]=encrypt(buffer+[b])
    return buffers.items()
def guess_bytes(randomprefixlen,ulen,blocksize):
    print(randomprefixlen,ulen,blocksize,"sretr")
    buffer=[0x41]*(blocksize-randomprefixlen%blocksize+blocksize-1)
    count=randomprefixlen//blocksize+1

    recoverbytes=[]
    for i in range(ulen):
        if len(recoverbytes)>0 and len(recoverbytes)%blocksize==0:
            count+=1
            buffer.extend([0x41]*blocksize)
       # print(len(encrypt(buffer[len(recoverbytes):])),len(encrypt(buffer[len(recoverbytes):]))//blocksize,blocksize)
        ciphertexts=generate_cipherexts(buffer[len(recoverbytes):]+recoverbytes)
        print(count,len(recoverbytes),len([encrypt(buffer[len(recoverbytes):])[c*blocksize:blocksize*(c+1)] for c in range(len(encrypt(buffer[len(recoverbytes):]))//blocksize)]),"****")#,[encrypt(buffer[len(recoverbytes):])[c*blocksize:blocksize*(c+1)] for c in range(len(encrypt(buffer[len(recoverbytes):]))//blocksize)][count])
        k=encrypt(buffer[len(recoverbytes):])
        ciphertext=[k[c*blocksize:blocksize*(c+1)] for c in range(len(k)//blocksize)]
        print(len(ciphertext),count)
        ciphertext=ciphertext[count]
        #print(len(ciphertext))
        for b, cipher in ciphertexts:
            if [cipher[blocksize*c:(c+1)*blocksize] for c in range(len(cipher)//blocksize)][count]==ciphertext:
                recoverbytes.append(b)
    return recoverbytes
rlen,ulen,blocksize=detect_blocksize()
unkonwn_str=guess_bytes(rlen,ulen,blocksize)
print(unkonwn_str)
"""

key = bytes(generate_randomdata(16))
iv = generate_randomdata(16)
def profile_for(string):
    string = string.replace(';', '_')
    string = string.replace('=', '_')
    return "comment1=cooking%20MCs;userdata=" + string + ";comment2=%20like%20a%20pound%20of%20bacon"
def parse_string(string):
    account = {}
    part = string.split(';')
    for kv in part:
        try:
            k,v = kv.split('=',1)
        except:
            k = kv
            v = ''
        account[k] = v
    return account
def encrypt(string):
    plaintext = profile_for(string)
    return cbc_encrypt(key, iv, addpaddaes(plaintext).decode())
def decrypt(ciphertext):
    plaintext = cbc_decrypt(key, iv, ciphertext)
    return parse_string(plaintext)
def attack():
    adminPlain = ";admin=true" #comment1=cooking%20MCs;userdata=_admin_true;comment2=%20like%20a%20pound%20of%20bacon
    ciphertext = encrypt(adminPlain)
    adminCipher = bytearray(ciphertext)
    #第一个'_'下标为32，CBC通过更改前一个块的对应内容即下标16，来更改'_' #第二个'_'下标为38，前一个块对应下标为22
    adminCipher[16] = adminCipher[16] ^ ord('_') ^ ord(';')
    adminCipher[22] = adminCipher[22] ^ ord('_') ^ ord('=')
    plaintext = decrypt((adminCipher))
    print (decrypt(ciphertext))
    print (plaintext )
attack()


