import hashlib
import os
import random
from time import time

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
e1 = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
      0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


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


def generate_random_value(max: int):
    random_data = int(hashlib.sha256(
        os.urandom(256) + (str(random.random()).encode()) + (str(time).encode()))
                      .hexdigest(), 16)

    return random_data % max


def generate_public_key(d: int):
    return double_and_add_point(e1, d)


def generate_private_key():
    private_key = generate_random_value(q)

    return private_key


def sign(M, d):
    r = generate_random_value(q-1) + 1

    P = double_and_add_point(e1, r)
    S1 = P[0] % q
    S2 = (int(hashlib.sha256(M.encode()).hexdigest(), 16) + d * S1) * extended_euclidian(q, r) % q

    return S1, S2


def verify(M, S1, S2, e2):
    S2_inverse = extended_euclidian(q, S2)
    A = (S2_inverse * int(hashlib.sha256(M.encode()).hexdigest(), 16)) % q
    B = (S1 * S2_inverse) % q

    A_e1 = double_and_add_point(e1, A)
    B_e2 = double_and_add_point(e2, B)

    T = add_point(A_e1[0], A_e1[1], B_e2[0], B_e2[1])

    print(f'\tA : {hex(A)}')
    print(f'\tB : {hex(B)}')

    return (T[0] % q) == (S1 % q)


if __name__ == "__main__":

    d = generate_private_key()
    e2 = generate_public_key(d)

    M = input("메시지? ")
    S1, S2 = sign(M, d)
    print("1. Sign:")
    print(f"\tS1 = {hex(S1)}")
    print(f"\tS2 = {hex(S2)}")

    print("2. 정확한 서명을 입력할 경우:")
    if verify(M, S1, S2, e2):
        print("검증 성공")
    else:
        print("검증 실패")

    print("3. 잘못된 서명을 입력할 경우:")
    if verify(M, S1 - 1, S2 - 1, e2):
        print("검증 성공")
    else:
        print("검증 실패")
