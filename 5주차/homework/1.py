import hashlib
from bitmap import BitMap

"""
m : filter size(비트 수)
k : 해시 함수의 수
n : Filter에 저장된 항목의 수
bf : Filter의 비트맵 (BitMap 클래스 이용)
"""


class BloomFilter:

    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.n = 0
        self.bf = BitMap(m)

    def getPositions(self, item):
        positions = []
        for i in range(1, self.k + 1):
            positions.append(int(hashlib.sha256((item + str(i)).encode()).hexdigest(), 16) % self.m)
        return positions

    def add(self, item):
        for pos in self.getPositions(item):
            self.bf.set(pos)
        self.n += 1

    def contains(self, item):
        for pos in self.getPositions(item):
            if not self.bf.test(pos):
                return False
        return True

    def reset(self):
        for i in range(self.m):
            self.bf.reset(i)

        self.n = 0

    def __repr__(self):
        return f"\
M = {self.m}, F = {self.k} \n\
BitMap = {self.bf.tostring()} \n\
항목의 수 = {self.n}, 1인 비트수 = {self.bf.count()} \n\
        "


if __name__ == "__main__":
    bf = BloomFilter(53, 3)

    for ch in "AEIOU":
        bf.add(ch)

    print(bf)
    for ch in "ABCDEFGHIJ":
        print(ch, bf.contains(ch))
