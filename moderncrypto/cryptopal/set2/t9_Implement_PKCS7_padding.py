

def implement_PKCS7_padding(data,size):
    n=size-len(data)%size
    if n==size:
        return data
    else:
        if str(type(data))=="<class 'str'>":
            data=data.encode()
        n=[n for i in range(n)]
        data=data+bytearray(n)
        return data

def implement_PKCS7_unpadding(data,size):
    n=data[-1]
    if n>=size:
        return data
    else:
        return data[:-n]

if __name__=='__main__':
    print(implement_PKCS7_padding("what's_up----",16))
    print(implement_PKCS7_unpadding(implement_PKCS7_padding("what's_up----",16),16))