import hashlib
import os
from random import random
from time import time


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


p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

if __name__ == '__main__':

    make_key = os.urandom(256) + (str(random()).encode()) + (str(time).encode())
    private_key = int(hashlib.sha256(make_key).hexdigest(), 16)

    while private_key > p:
        make_key = os.urandom(256) + (str(random()).encode()) + (str(time).encode())
        private_key = int(hashlib.sha256(make_key).hexdigest(), 16)

    print('개인키(16진수) :', hex(private_key))
    print('개인키(16진수) :', private_key, end='\n\n')

    public_key = double_and_add_point(G, private_key)

    print(f'공개키(16진수) : ({hex(public_key[0])}, {hex(public_key[1])})')
    print('공개키(10진수) :', public_key)
