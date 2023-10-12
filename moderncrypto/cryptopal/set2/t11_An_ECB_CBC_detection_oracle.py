from t10_Implement_CBC_mode import aes_ecb_encrypt,aes_cbc_encrypt
from random import randint
from Crypto.Cipher.AES import block_size
from Crypto import Random

class AesencryptionOracle:
    @staticmethod
    def encrypt(plaintext):
        padded_plaintext=AesencryptionOracle._pad_with_bytes(plaintext)
        key = Random.new().read(block_size)
        if randint(0,1):
            return "CBC",aes_cbc_encrypt(padded_plaintext,key,Random.new().read(block_size))
        else:
            return "ECB",aes_ecb_encrypt(padded_plaintext,key)
    @staticmethod
    def _pad_with_bytes(binary_data):
        return Random.new().read(randint(5,10))+binary_data+Random.new().read(randint(5,10))

def count_aes_ecb_repetitions(ciphertext):
    chunks=[ciphertext[i:i+block_size] for i in range(0,len(ciphertext),block_size)]
    number_of_duplicates=len(chunks)-len(set(chunks))
    return number_of_duplicates

def detect_cipher(ciphertext):
    if count_aes_ecb_repetitions(ciphertext)>0:
        return 'ECB'
    else:
        return 'CBC'

def main():
    oracle=AesencryptionOracle()
    inputdata=bytes([0]*64)
    for _ in range(1000):
        encryption_used,ciphertext=oracle.encrypt(inputdata)
        encryption_detected = detect_cipher(ciphertext)
        assert encryption_used == encryption_detected

if __name__=='__main__':
    main()