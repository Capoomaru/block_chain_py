import random
import string


def get_alphabet_list_and_shuffled_list():
    original_list = list(string.ascii_lowercase)
    mixed_list = list(string.ascii_lowercase)
    for _ in range(1, random.randint(1, 10)):
        random.shuffle(mixed_list)

    return original_list, mixed_list


def encryption(plain_text: str):
    cipher_text = ''
    for alphabet in plain_text:
        cipher_text += E.get(alphabet, alphabet)
    return cipher_text


def decryption(cipher_text: str):
    plain_text = ''
    for alphabet in cipher_text:
        plain_text += D.get(alphabet, alphabet)
    return plain_text


if __name__ == '__main__':
    # 입력 구문
    plain_input = input('평문 입력 : ')

    # 알파벳 shuffle
    key_list, value_list = get_alphabet_list_and_shuffled_list()

    # dictionary 선언
    E = dict()
    for i in range(len(key_list)):
        E[key_list[i]] = value_list[i]

    D = dict()
    for key in E.keys():
        D[E[key]] = key

    # 출력 구문
    encrypted_text = encryption(plain_input)
    print(f'암호문 : ' + encrypted_text)

    decrypted_text = decryption(encrypted_text)
    print(f'해독문 : ' + decrypted_text)
