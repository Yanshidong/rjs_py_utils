import random
import string


class RjsRandom:
    @staticmethod
    def random_letter_lower(length_random: int = 4, preffix: str = "", suffix: str = ""):
        return preffix+(''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f','e', 'd', 'c', 'b', 'a'], length_random)))+suffix

    def random_num(self):
        return 1
