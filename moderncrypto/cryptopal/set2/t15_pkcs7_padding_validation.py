

def is_pkcs7_padding(data):
    padding = data[- data[-1]:]
    padding=(list(padding))
    try:
        if sum(padding)==len(padding)*padding[-1]:
            return True
        else:
            return False
    except Exception as e:
        print("The padding is not pkcs#7",e)
        return False

if __name__ == "__main__":
    print(is_pkcs7_padding(b"ICE ICE BABY\x04\x04\x04\x04"))
    print(is_pkcs7_padding(b"ICE ICE BABY\x05\x05\x05\x05"))
    print(is_pkcs7_padding(b"ICE ICE BABY\x01\x32\x03\x03"))
    print(is_pkcs7_padding(b"ICE ICE BABY!\x03\x03\x03"))