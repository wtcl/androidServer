import random
from produce_pskey import getkey
from sm2_source import SM2
from base64 import b64encode, b64decode

# sm2的公私钥
content = input("请输入明文： ")
SM2_PRIVATE_KEY, SM2_PUBLIC_KEY = getkey()
sm2_crypt = SM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)
# 加密
def encrypt(info):
    encode_info = sm2_crypt.encrypt(info.encode(encoding="utf-8"))
    encode_info = b64encode(encode_info).decode()  # 将二进制bytes通过base64编码
    return encode_info


# 解密
def decrypt(info):
    decode_info = b64decode(info.encode())  # 通过base64解码成二进制bytes
    decode_info = sm2_crypt.decrypt(decode_info).decode(encoding="utf-8")
    return decode_info


encrypted_info = encrypt(content)
print('密文C: ', encrypted_info)

decrypted_info = decrypt(encrypted_info)
print('明文m: ', decrypted_info)
