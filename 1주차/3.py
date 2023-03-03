from cryptography.fernet import Fernet


def read_file_to_bytes(filename):
    try:
        file = open(filename, 'r')
        data = file.read()

        if type(data) != bytes:
            data = data.encode()
    finally:
        file.close()

    return data


def write_file_to_str(filename, data):
    try:
        file = open(filename, 'w')

        if type(data) != str:
            data = data.decode()

        file.write(data)
    finally:
        file.close()


if __name__ == '__main__':
    # Fernet 생성
    key = Fernet.generate_key()
    f = Fernet(key)

    # 파일 byte로 읽어오기
    input_bytes = read_file_to_bytes('data.txt')
    # 파일 암호화
    encrypted_data = f.encrypt(input_bytes)
    # 암호화된 내용 저장하기
    write_file_to_str('encrypted.txt', encrypted_data)
    # 저장한 암호화 내용 불러오기
    encrypted_bytes = read_file_to_bytes('encrypted.txt')
    # 암호화 내용 복호하기
    decrypted_data = f.decrypt(encrypted_bytes).decode()
    # 출력하기
    print(decrypted_data)
