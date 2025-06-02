from string import ascii_uppercase


class Reflector:
    def __init__(self, wiring):
        self.left = ascii_uppercase
        self.right = wiring

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal
