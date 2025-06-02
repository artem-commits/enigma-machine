from string import ascii_uppercase


class Plugboard:

    def __init__(self, pairs):
        self.left = ascii_uppercase
        self.right = ascii_uppercase

        for pair in pairs:
            a = pair[0]
            b = pair[1]
            pos_a = self.left.find(a)
            pos_b = self.left.find(b)
            self.left = self.left[0:pos_a] + b + self.left[pos_a + 1:]
            self.left = self.left[0:pos_b] + a + self.left[pos_b + 1:]

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal
