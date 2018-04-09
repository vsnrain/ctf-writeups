import hashlib
import math

start = 97
end = 122

flg = "1d9c0db55855bc6478a047c9"

mx = int("ffffff", 16)

def square_distance(a):
    s = 0
    for i in a:
        s += i*i
    return s

for a1 in range(start, end):
    for a2 in range(start, end):
        for a3 in range(start, end):
            for a4 in range(start, end):
                for a5 in range(start, end):
                    psw = "INSA{" + chr(a1) + chr(a2) + chr(a3) + chr(a4) + chr(a5) + "}"
                    hsh = hashlib.sha1(psw).hexdigest()

                    p = []
                    for i in range(0, 12, 2):
                        a = flg[i:i+1]
                        b = hsh[i:i+1]
                        x = abs(int(a, 16) - int(b, 16))
                        p.append(x)

                    xx = square_distance(p)

                    if xx < mx:
                        mx = xx
                        print xx
                        print psw
