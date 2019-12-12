from math import log2, ceil, sqrt


def bytes_from_file(filename, chunksize=2**13):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break


def blocks_from_file(filename, chunksize=2**13):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                yield chunk
            else:
                break


def make_ascii_key(key):
    result = bytearray()
    for i in range(len(key)):
        result.append(int(key[i]))
    return result


def rsa_encode(filename, p, q, close_key):
    number = p * q
    euler_fun = (p - 1) * (q - 1)
    length = ceil(log2(number) / 8)
    open_key = expended_Euklid_algoritm(euler_fun, close_key)
    if open_key < 0:
        open_key += euler_fun
    file_out = open(filename + '.cph', 'wb')
    b_arr = bytearray()
    for b in bytes_from_file(filename):
        result = fast_multiplying(b, open_key, number)
        bi_result = str(bin(result))[2:]
        bi_result = bi_result.zfill(length * 8)
        for i in range(length):
            numb = int(bi_result[i * 8:(i + 1) * 8], 2)
            b_arr.append(numb)
    file_out.write(b_arr)
    file_out.close()
    return open_key


def rsa_decode(filename, r, close_key):
    length = ceil(log2(r) / 8)
    if filename[len(filename) - 4:] == '.cph':
        filetemp = filename[:(len(filename) - 4)]
        temp = filetemp.partition('.')
        filetemp = temp[0] + '(copy)' + temp[1] + temp[2]
        file_out = open(filetemp, 'wb')
    else:
        filetemp = filename + '.cph'
        file_out = open(filetemp, 'wb')
    b_arr = bytearray()
    for b in blocks_from_file(filename, length):
        number = int.from_bytes(b, byteorder='big')
        result = fast_multiplying(number, close_key, r)
        if result > 255:
            return 1
        b_arr.append(result)
    file_out.write(b_arr)
    file_out.close()


def Euklid_algoritm(a, b):
    temp = [a, b]
    while temp[0] != temp[1] and min(temp) != 0:
        temp[0], temp[1] = temp[1], temp[0] % temp[1]
    return temp[0]


def expended_Euklid_algoritm(a, b):
    d = [a, b]
    x = [1, 0]
    y = [0, 1]
    while d[1] > 1:
        q = d[0] // d[1]
        d.append(d[0] % d[1])
        x.append(x[0] - q * x[1])
        y.append(y[0] - q * y[1])
        d.pop(0)
        x.pop(0)
        y.pop(0)
    return y[1]


def fast_multiplying(a, digree, number):
    x = 1
    while digree != 0:
        while digree % 2 == 0:
            digree //= 2
            a = (a**2) % number
        digree -= 1
        x = (x * a) % number
    return x


def find_euler_fun(number):
    dividers = set()
    i = 2
    temp = number
    while i <= int(sqrt(temp)):
        while temp % i == 0:
            dividers.add(i)
            temp //= i
        i += 1
    if temp > 1:
        dividers.add(temp)
    for divider in dividers:
        number = number // divider * (divider - 1)
    return number
