class AdditiveCipher:

    def __init__(self, key: int):
        self.__key = key

    def encrypt(self, plain_text: str):
        encrypted_text = ''

        for plain_chr in plain_text:
            encrypted_text += chr((ord(plain_chr) + self.__key) % 26 + ord('A'))

        return encrypted_text


if __name__ == '__main__':
    print("hello")
    additiveCipher = AdditiveCipher(-5)
    print(additiveCipher.encrypt("hello"))
