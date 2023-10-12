from base64 import b64decode
from Crypto.Cipher import AES
from t9_Implement_PKCS7_padding import implement_PKCS7_padding,implement_PKCS7_unpadding

with open('10.txt','r',encoding='utf-8') as f:
    con=f.read()

con=(b64decode(con))
# print(list(con))

def aes_ecb_encrypt(data,key):
    c=AES.new(key,AES.MODE_ECB)
    return c.encrypt(implement_PKCS7_padding(data,AES.MODE_ECB))

def xor_data(bd1,bd2):
    # print(bd1,'\n',bd2)
    return bytes([b1^b2 for b1,b2 in zip(bd1,bd2)])

def aes_cbc_encrypt(data,key,iv):
    c=b''
    prev=iv
    for i in range(0,len(data),AES.block_size):
        current_plaintext_block=implement_PKCS7_padding(data[i:i+AES.block_size],AES.block_size)
        block_cipher_input=xor_data(current_plaintext_block,prev)
        encrypted_block=aes_ecb_encrypt(block_cipher_input,key)
        c+=encrypted_block
        prev=encrypted_block
    return c

def aes_ecb_decrypt(data,key):
    c=AES.new(key,AES.MODE_ECB)
    return c.decrypt(data)

def aes_cbc_decrypt(data,key,iv):
    p=b''
    prev=iv
    for i in range(0,len(data),int(AES.block_size)):
        current_cipher_block=data[i:i+int(AES.block_size)]
        decrypted_block=aes_ecb_decrypt(current_cipher_block,key)
        p+=xor_data(prev,decrypted_block)
        prev=current_cipher_block
    return implement_PKCS7_unpadding(p,AES.block_size)
def main():
    iv=b'\x00'+bytearray([AES.block_size])
    key=b"YELLOW SUBMARINE"
    print(aes_cbc_decrypt(con,key,iv).decode().rstrip())

if __name__=='__main__':
    main()

# https://zhuanlan.zhihu.com/p/149989030