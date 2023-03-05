import string


class Vigenere:
    key: str

    def __init__(self, key: str):
        self.key = key.upper()
        self.key_size = len(self.key)
        self.key_int_list = list()
        for i in range(self.key_size):
            self.key_int_list.append(ord(self.key[i]) - ord('A'))

    def encrypt(self, plain_text: str):
        encrypted_text = ''

        for text_index in range(len(plain_text)):
            key_index = text_index % self.key_size
            offset = (ord(plain_text[text_index]) + self.key_int_list[key_index] - ord('A')) % len(
                string.ascii_uppercase)
            encrypted_text += chr(ord('A') + offset)
        return encrypted_text

    def decrypt(self, encrypted_text: str):
        decrypted_text = ''

        for text_index in range(len(encrypted_text)):
            key_index = text_index % self.key_size
            offset = (ord(encrypted_text[text_index]) - self.key_int_list[key_index] - ord('A')) % len(
                string.ascii_uppercase)
            decrypted_text += chr(ord('A') + offset)
        return decrypted_text


class Autokey:
    key: int

    def __init__(self, key: int):
        self.key = key

    def encrypt(self, plain_text: str):
        encrypted_text = ''

        tmp_key = self.key
        for item in plain_text:
            value = (tmp_key + ord(item) - ord('A')) % len(string.ascii_uppercase)
            tmp_key = ord(item) - ord('A')
            encrypted_text += chr(value + ord('A'))

        return encrypted_text

    def decrypt(self, encrypted_text: str):
        decrypted_text = ''

        tmp_key = self.key
        for item in encrypted_text:
            value = (ord(item) - ord('A') - tmp_key) % len(string.ascii_uppercase)
            tmp_key = value
            decrypted_text += chr(value + ord('A'))

        return decrypted_text


if __name__ == '__main__':
    # 입력 구문
    plain_input = input('평문 입력 : ').upper().replace(' ', '')

    # vigenere 코드
    vigenere_key = input('Vigenere 암호 : ').upper()
    vigenere = Vigenere(key=vigenere_key)

    vigenere_encrypted = vigenere.encrypt(plain_text=plain_input)
    print('Vigenere 암호문 : ' + vigenere_encrypted)

    vigenere_decrypted = vigenere.decrypt(vigenere_encrypted)
    print('Vigenere 해독문 : ' + vigenere_decrypted)

    # autokey 코드
    auto_key_input = int(input('자동 키 암호 입력 : '))
    autokey = Autokey(key=auto_key_input)

    autokey_encrypted = autokey.encrypt(plain_text=plain_input)
    print('autokey 암호문 : ' + autokey_encrypted)

    autokey_decrypted = autokey.decrypt(encrypted_text=autokey_encrypted)
    print('autokey 해독문 : ' + autokey_decrypted)
