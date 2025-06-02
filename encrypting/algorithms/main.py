from keyboard import Keyboard
from plugboard import Plugboard
from rotor import Rotor
from reflector import Reflector
from enigma import Enigma

# historical enigma rotors and reflectors
I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
V = Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
A = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
B = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
C = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')

# keyboard and plugboard
KB = Keyboard()
PB = Plugboard(['AR', 'GK', 'OX'])

# define enigma machine
ENIGMA = Enigma(B, I, II, III, PB, KB)

# set the rings
ENIGMA.set_rings((1, 1, 1))

# set message key
ENIGMA.set_key('DOG')

# encipher a letter
message = 'TEST'
cipher_text = ''
for letter in message:
    cipher_text = cipher_text + ENIGMA.encipher(letter)
print(cipher_text)
