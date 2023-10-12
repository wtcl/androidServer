import sm2_source
import random

# 继承SM2类
class Generator_SM2_Key(sm2_source.SM2):
    def __init__(self, private_key=None, public_key=None, ecc_table=sm2_source.default_ecc_table, mode=0):
        super().__init__(private_key, public_key, ecc_table)

    def get_private_key(self):
        self.private_key = hex(random.randint(1,int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',16)-2))[2:]  # d∈[1, n-2]
        return self.private_key

    def get_public_key(self):
        self.public_key = self._kg(int(self.private_key, 16), self.ecc_table['g'])  # P=[d]G
        return self.public_key


def getkey():
    sm2key = Generator_SM2_Key()
    private_key = sm2key.get_private_key()
    print('private_key:', private_key)
    public_key = sm2key.get_public_key()
    print('public_key: ', public_key)
    return private_key,public_key