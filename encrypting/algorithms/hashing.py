def simple_hash(text: str) -> int:
    hash_value = 0
    for char in text:
        hash_value = (hash_value * 31 + ord(char)) & 0xFFFFFFFF
    return hash_value