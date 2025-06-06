import itertools
import string
from typing import Optional, Tuple


def simple_hash(text: str) -> int:
    """
    Простая хеш-функция, основанная на сумме байтов и битовых операциях.
    Возвращает 32-битное целое число.
    """
    hash_value = 0
    for char in text:
        # Обновляем хеш: текущий хеш * 31 + ASCII-код символа
        hash_value = (hash_value * 31 + ord(char)) & 0xFFFF
    return hash_value


def find_collision(target_hash: int, max_length: int = 4) -> Tuple[Optional[str], Optional[int]]:
    """
    Ищет строку, хеш которой совпадает с целевым хешем.
    """
    chars = string.ascii_lowercase

    lst = []

    for length in range(1, max_length + 1):
        for candidate in itertools.product(chars, repeat=length):
            candidate_str = ''.join(candidate)
            candidate_hash = simple_hash(candidate_str)
            if candidate_hash == target_hash:
                print(candidate_str, candidate_hash)
                lst.append((candidate_str, candidate_hash))

    return lst
