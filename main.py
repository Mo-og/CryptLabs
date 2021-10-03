import random
from itertools import cycle

MAX_NUM = 255
CHARS_IN_UTF = 255  # 137994


def decrypt(text: str, gamma):
    result = ''
    for i in range(len(text)):
        l = (ord(text[i]) ^ gamma[i]) % CHARS_IN_UTF
        result += chr(l)
    return result


def get_byte(c_num: int = -1, char: str = None):
    if c_num == -1:
        c_num = ord(char)
    a = [0, 0, 0, 0, 0, 0, 0, 0]
    c = a
    if c_num > 255:
        for i in range(c_num // 255 - 1):
            c += a
        if c_num % 255 > 0:
            c += a

    ch_bin = bin(c_num)[2:]
    for i in range(len(ch_bin)):
        c[len(c) - 1 - i] = int(ch_bin[i])
    c_str = ''
    for n in c:
        c_str += str(n)
    return c_str


def crypt(text: str, key: str):
    result = ''
    random.seed(key)
    rand = []
    lets = []
    for x in text:
        if not x:
            break
        r = random.randint(0, MAX_NUM)
        rand.append(r)
        lets.append(ord(x))
        result += chr((ord(x) ^ r) % CHARS_IN_UTF)  # всё к-во символов в таблице кодировки
    return result


def get_letters_codes(text):
    result = []
    for c in text:
        result.append(ord(c))
    return result


key = 'whatever text is here is a key 7128%*$^#'
phrase = 'Текстовая фраза'

print("Исходный текст: '" + phrase + "'")
u = crypt(phrase, key)
print("Зашифрованый текст: '" + str(u) + "'")
print("Расшифрованый текст: '" + str(crypt(u, key)) + "'")

a = get_letters_codes(phrase)  # коды чистого текста
b = get_letters_codes(crypt('Чеснок это овощ', key))  # коды зашифрованого текста (желаемый левый вариант)
c = []
for (x, y) in zip(a, cycle(b)):
    c.append(x ^ y)  # операция xor этих кодов даст гамму, которой нужно гамировать зашифрованный чистый текст,
    # чтобы получить при расшифровке указанный желаемый левый
s = ''
for i in c:
    s += "%d " % i
print('Пример гаммы для некорректной расшифровки:\n' + s[:-2])
s = decrypt(crypt(phrase, key), c)
print("Фраза, расшифрованная этой гаммой:'" + s + "'")
