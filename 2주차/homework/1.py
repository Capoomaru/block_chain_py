from cryptography.fernet import Fernet as Aes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

MAX_LEN = 190


def get_public_key():
    with open('public_key.pem', 'rb') as public_file:
        public_key = serialization.load_pem_public_key(
            public_file.read(),
            backend=default_backend()
        )
    return public_key


def get_private_key():
    with open('private_key.pem', 'rb') as private_file:
        private_key = serialization.load_pem_private_key(
            private_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def encrypt_rsa(key, msg):
    enc_msg = key.encrypt(
        msg,
        padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return enc_msg


def decrypt_rsa(key, enc_msg):
    dec_msg = key.decrypt(
            enc_msg,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    return dec_msg


if __name__ == '__main__':
    public_key = get_public_key()
    private_key = get_private_key()

    origin_msg = input('전송할 메시지를 입력하세요 : ')

    if len(origin_msg.encode()) > MAX_LEN:
        print("AES 방식을 이용하여 메시지 암호화 및 RSA 방식을 이용하여 AES 키 암호화")
        # DO 암호문 = encrypt(AES(eng_msg))
        enc_aes_key = Aes.generate_key()
        enc_aes = Aes(enc_aes_key)
        enc_msg = enc_aes.encrypt(origin_msg.encode())

        # DO 암호문_키 = encrypt(ENC(aes_key - 공개키))
        enc_key = encrypt_rsa(public_key, enc_aes_key)

        # DO enc_msg와 enc_key를 insecure channel로 수신자에게 전달

        # DO 복호문_키 = decrypt(ENC(enc_key - 개인키))
        dec_aes_key = decrypt_rsa(private_key, enc_key)

        # DO 복호문(dec_msg) => decrypt(AES(aes_key))
        dec_aes = Aes(dec_aes_key)
        dec_msg = dec_aes.decrypt(enc_msg)

        print(dec_msg.decode())

    else:
        print("RSA 방식을 이용하여 메세지 암호화")
        # DO ENC
        enc_msg = encrypt_rsa(public_key, origin_msg.encode())

        # DO enc_msg를 insecure channel로 수신자에게 전달

        # DO 복호문(dec_msg) => decrypt(enc_msg, key=private_key)
        dec_msg = decrypt_rsa(private_key, enc_msg)

    print(f'원본 메세지 : \n{origin_msg}')
    print(f'해석된 메시지 : \n{dec_msg.decode()}')
    print(f'메시지 일치 여부 : {origin_msg == dec_msg.decode()}')
