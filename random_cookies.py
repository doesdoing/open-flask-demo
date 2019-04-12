import random


def random_cookies(num):
    B = ""
    A = random.sample(
        'qwertyuiopasdfghjklzxcvbnm7894561230\\/?.>,<;:|{}[]~!@#$%^&*()', int(num > 50 and 50 or num))
    for x in range(len(A)):
        B = B + A[x]
    return B



