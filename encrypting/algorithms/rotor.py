from string import ascii_uppercase


class Rotor:
    def __init__(self, wiring, notch):
        self.left = ascii_uppercase
        self.right = wiring
        self.notch = notch

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

    def show(self):
        print(self.left)
        print(self.right)
        print("")

    def rotate(self, n=1, forward=True):
        for i in range(n):
            if forward:
                self.left = self.left[1:] + self.left[0]
                self.right = self.right[1:] + self.right[0]
            else:
                self.left = self.left[25] + self.left[:25]
                self.right = self.right[25] + self.right[:25]

    def rotate_to_letter(self, letter):
        n = ascii_uppercase.find(letter)
        self.rotate(n)

    def set_ring(self, n):

        # rotate the rotor backwards
        self.rotate(n-1, forward=False)

        # adjust the turnover notch in relationship to the wiring
        n_notch = ascii_uppercase.find(self.notch)
        self.notch = ascii_uppercase[(n_notch - (n - 1)) % 26]
