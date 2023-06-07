import random
import math

class RSAUtils:
    def __init__(self):
        self.prime = set()
        self.public_key = None
        self.private_key = None
        self.n = None

    def primefiller(self):
        seive = [True] * 250
        seive[0] = False
        seive[1] = False

        for i in range(2, 250):
            for j in range(i * 2, 250, i):
                seive[j] = False

        for i in range(len(seive)):
            if seive[i]:
                self.prime.add(i)

    def pickrandomprime(self):
        k = random.randint(0, len(self.prime) - 1)
        it = iter(self.prime)
        for _ in range(k):
            next(it)

        ret = next(it)
        self.prime.remove(ret)
        return ret

    def setkeys(self):
        prime1 = self.pickrandomprime()
        prime2 = self.pickrandomprime()

        self.n = prime1 * prime2
        fi = (prime1 - 1) * (prime2 - 1)

        e = 2
        while True:
            if math.gcd(e, fi) == 1:
                break
            e += 1

        self.public_key = e

        d = 2
        while True:
            if (d * e) % fi == 1:
                break
            d += 1

        self.private_key = d

    def encrypt(self, message):
        e = self.public_key
        encrypted_text = 1
        while e > 0:
            encrypted_text *= message
            encrypted_text %= self.n
            e -= 1
        return encrypted_text

    def decrypt(self, encrypted_text):
        d = self.private_key
        decrypted = 1
        while d > 0:
            decrypted *= encrypted_text
            decrypted %= self.n
            d -= 1
        return decrypted

    def encoder(self, message):
        encoded = []
        for letter in message:
            encoded.append(self.encrypt(ord(letter)))
        return encoded

    def decoder(self, encoded):
        s = ''
        for num in encoded:
            s += chr(self.decrypt(num))
        return s
