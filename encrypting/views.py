from django.shortcuts import render
from .forms import EnigmaForm
from .algorithms.enigma import Enigma
from .algorithms.rotor import Rotor
from .algorithms.reflector import Reflector
from .algorithms.plugboard import Plugboard
from .algorithms.keyboard import Keyboard

def encipher_view(request):
    if request.method == 'POST':
        form = EnigmaForm(request.POST)
        if form.is_valid():
            # Get form data
            rotor_r1 = form.cleaned_data['rotor_r1']
            rotor_r2 = form.cleaned_data['rotor_r2']
            rotor_r3 = form.cleaned_data['rotor_r3']
            reflector = form.cleaned_data['reflector']
            position_r1 = form.cleaned_data['position_r1']
            position_r2 = form.cleaned_data['position_r2']
            position_r3 = form.cleaned_data['position_r3']
            ring_r1 = int(form.cleaned_data['ring_r1'])
            ring_r2 = int(form.cleaned_data['ring_r2'])
            ring_r3 = int(form.cleaned_data['ring_r3'])
            plugboard_pairs = form.cleaned_data['plugboard_pairs']
            message = form.cleaned_data['message'].upper()

            # Create rotors
            rotors = {
                'I': Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
                'II': Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
                'III': Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
                'IV': Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
                'V': Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
            }

            # Create reflectors
            reflectors = {
                'A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
                'B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
            }

            # Create plugboard
            plugboard_pairs = [pair.strip() for pair in plugboard_pairs.split() if pair.strip()]
            pb = Plugboard(plugboard_pairs)

            # Create keyboard
            kb = Keyboard()

            # Create Enigma machine
            enigma = Enigma(
                reflectors[reflector],
                rotors[rotor_r1],
                rotors[rotor_r2],
                rotors[rotor_r3],
                pb,
                kb
            )

            # Set rings
            enigma.set_rings((ring_r1, ring_r2, ring_r3))

            # Set initial positions
            enigma.set_key(position_r1 + position_r2 + position_r3)

            # Encrypt message
            encrypted_message = ''
            for letter in message:
                if letter.isalpha():
                    encrypted_message += enigma.encipher(letter)
                else:
                    encrypted_message += letter

            return render(request, 'encrypting/enigma.html', {
                'form': form,
                'encrypted_message': encrypted_message
            })
    else:
        form = EnigmaForm()

    return render(request, 'encrypting/enigma.html', {'form': form})

