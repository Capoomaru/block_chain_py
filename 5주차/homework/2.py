import hashlib
import time


def getTarget(targetBits):
    exponent = targetBits >> 24
    coefficient = targetBits % 2**24
    return coefficient * 2**(8*(exponent-3)), 8*(exponent-3)


def proof_of_work(header, target):

    while True:
        extra_nonce = int(time.time())
        for nonce in range(max_nonce):
            h = hashlib.sha256()
            h.update((header+str(extra_nonce)+str(nonce)).encode())
            hash_result = h.hexdigest()

            if int(hash_result, 16) < target:
                print(f"메시지: {header}, Extra nonce: {extra_nonce}, nonce: {nonce}")
                return hash_result, nonce


max_nonce = 2 ** 32

if __name__ == "__main__":
    msg = input("메시지의 내용은? : ")
    targetBits = int(input("Target bits? : "), 16)

    target, rightBits = getTarget(targetBits)
    difficulty_bits = 256 - rightBits - 24

    start_time = time.time()

    print(f"Target bits: 0x{format(target, '064x')}")
    hash_result, nonce = proof_of_work(msg, target)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"실행 시간: {elapsed_time}초")
    print(f"Hash result: 0x{int(hash_result, 16):064x}")
