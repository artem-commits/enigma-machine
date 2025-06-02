from string import ascii_uppercase


class Keyboard:

    def forward(self, letter):
        alphabet = ascii_uppercase
        signal = alphabet.find(letter)
        return signal

    def backward(self, signal):
        alphabet = ascii_uppercase
        letter = alphabet[signal]
        return letter
