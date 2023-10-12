import hashlib
import itertools
import time


starttime = time.time()
hash1="67ae1a64661ac8b4494666f58c4822408dd0a3e4"
for str3 in itertools.product(['Q', 'q'],[ 'W', 'w'],[ '%', '5'], ['8', '('],[ '=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']):
    newS = "".join(str3)
    for i in itertools.permutations(newS, 8):
        if hashlib.sha1(("".join(i)).encode('utf-8')).hexdigest() == hash1:
            print("".join(i))
            endtime = time.time()
            print((endtime - starttime))
            exit(0)