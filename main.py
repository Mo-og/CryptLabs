import math
import random
from itertools import cycle

MAX_NUM = 255
CHARS_IN_UTF = 255  # 137994


def get_byte(char: str = None, num: int = -1):
    if num == -1:
        num = ord(char)
    # print("ch=", char, "num=", num)
    a = [0, 0, 0, 0, 0, 0, 0, 0]
    c = [0, 0, 0, 0, 0, 0, 0, 0]
    log = math.log2(num)
    log8 = int(log // 8)
    if log8 > 0:
        for i in range(log8 - 1):
            c += a
        if log % 8 != 0:
            c += a
    ch_bin = bin(num)[2:]
    for i in range(len(ch_bin)):
        c[len(c) - 1 - i] = int(ch_bin[len(ch_bin) - 1 - i])
    c_str = ''
    for n in c:
        c_str += str(n)
    return c_str


def crypt(text: str, key: str='', debug=False, gamma=None):
    result = ''
    rands = []
    if gamma is not None:
        rands = gamma
    else:
        random.seed(key)
        for i in range(len(text)):
            rands.append(random.randint(0, MAX_NUM))
        # if decrypt: rands.reverse()
    for x in range(len(text)):
        r = rands[x]
        char = get_byte(char=text[x])
        debug_ch = "ch = " + char + " // = "
        char = int(char, 2)
        debug_ch += str(char) + " = " + text[x]
        debug_rand = "rd = " + get_byte(num=r) + " // = " + str(r)
        result += chr(char ^ r)  # всё к-во символов в таблице кодировки
        debug_res = "rs = " + get_byte(chr(char ^ r)) + " // = " + str(char ^ r)
        if debug: print(debug_ch + '\n' + debug_rand + '\n' + debug_res)
    return result


def get_letters_codes(text):
    result = []
    for c in text:
        result.append(ord(c))
    return result


key = '111'
phrase = 'hello world'

print("Исходный текст: '" + phrase + "'")
u = crypt(phrase, key, True)
print("Зашифрованый текст: '" + str(u) + "'")
print("Расшифрованый текст: '" + str(crypt(u, key, True)) + "'")

a = get_letters_codes(phrase)  # коды чистого текста
b = get_letters_codes(crypt('unknown tax', key))  # коды зашифрованого текста (желаемый левый вариант)
c = []
for (x, y) in zip(a, cycle(b)):
    c.append(x ^ y)  # операция xor этих кодов даст гамму, которой нужно гамировать зашифрованный чистый текст,
    # чтобы получить при расшифровке указанный желаемый левый
s = ''
for i in c:
    s += "%d " % i
print('Пример гаммы для некорректной расшифровки:\n' + s[:-2])
s = crypt(crypt(phrase, key), gamma=c)
print("Фраза, расшифрованная этой гаммой:'" + s + "'")
