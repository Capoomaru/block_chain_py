import hashlib
from Crypto.Hash import RIPEMD160
import base58check


def extended_euclidian(a, b):
    t1 = 0
    t2 = 1
    r1 = a
    r2 = b

    while r2 > 0:
        q = r1 // r2
        r = r1 - q * r2
        r1 = r2
        r2 = r

        t = t1 - q * t2
        t1 = t2
        t2 = t

    if r1 == 1:
        return t1


def add_point(x1, y1, x2, y2):
    if x1 > x2:
        tmp = x1
        x1 = x2
        x2 = tmp

        tmp = y1
        y1 = y2
        y2 = tmp

    m = ((y2 - y1) * extended_euclidian(p, (x2 - x1))) % p
    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return x3, y3


def double_point(x, y):
    m = ((3 * (x ** 2)) * extended_euclidian(p, (2 * y))) % p
    x3 = (m ** 2 - x * 2) % p
    y3 = (m * (x - x3) - y) % p

    return x3, y3


def double_and_add_point(point, n):
    x = point[0]
    y = point[1]

    for i in range(len(bin(n)) - 4, -1, -1):
        x, y = double_point(x, y)
        if ((n >> i) & 1) == 1:
            x, y = add_point(x, y, point[0], point[1])

    return x, y


def compress_pubkey(public_key):
    is_odd = public_key[1] % 2

    comp_key = ('03' if is_odd else '02')
    comp_key += '0' * (64 - len(hex(public_key[0])[2:]))
    comp_key += hex(public_key[0])[2:]

    return comp_key


p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
e1 = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
      0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

if __name__ == '__main__':
    private_key = int(input("개인키 입력 : "), 16)

    public_key = double_and_add_point(e1, private_key)

    comp_pubkey = compress_pubkey(public_key)

    public_hash = '00'+RIPEMD160.new(hashlib.sha256(bytes.fromhex(comp_pubkey)).digest()).hexdigest()

    print(f'공개키 hash = {public_hash[2:]}')

    mid = public_hash + hashlib.sha256(hashlib.sha256(bytes.fromhex(public_hash)).digest()).hexdigest()[:8]
    bitcoin_address = base58check.b58encode(bytes.fromhex(mid)).decode()

    print(f'비트코인 주소 = {bitcoin_address}')
