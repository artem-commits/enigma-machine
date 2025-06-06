from django.shortcuts import render, redirect
from .forms import EnigmaForm, DecryptForm
from .algorithms.enigma import Enigma
from .algorithms.rotor import Rotor
from .algorithms.reflector import Reflector
from .algorithms.plugboard import Plugboard
from .algorithms.keyboard import Keyboard
import time
import itertools
import string
from .algorithms.hash import simple_hash, find_collision
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse


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


def decrypt_view(request):
    if request.method == 'POST':
        form = DecryptForm(request.POST)
        if form.is_valid():
            # Get form data
            encrypted_message = form.cleaned_data['encrypted_message'].upper()
            known_text = form.cleaned_data['known_text'].upper()
            max_attempts = form.cleaned_data['max_attempts']
            known_reflector = form.cleaned_data['reflector']

            # Create keyboard and empty plugboard
            kb = Keyboard()
            pb = Plugboard([])

            # Настройки для перебора
            reflector_list = [known_reflector] if known_reflector is not '' else ['A', 'B', 'C']
            rotor_combos = list(itertools.permutations(['I', 'II', 'III'], 3))
            positions = list(itertools.product('ABCDEFG', repeat=3))
            rings = [(1, 1, 1)]  # фиксированные кольцевые настройки

            start_time = time.time()
            attempts = 0
            found = False  # флаг успешного нахождения

            for reflector_name in reflector_list:
                print("Пробуем рефлектор:", reflector_name)
                for rotor_combo in rotor_combos:
                    print("Комбинация роторов:", rotor_combo)
                    for pos1, pos2, pos3 in list(positions):
                        print("Позиции:", pos1, pos2, pos3)
                        for ring1, ring2, ring3 in rings:
                            if attempts >= max_attempts:
                                found = False
                                break

                            reflectors = {
                                'A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
                                'B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                                'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
                            }

                            rotor_definitions = {
                                'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
                                'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
                                'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
                                'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
                                'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
                            }

                            r1 = Rotor(*rotor_definitions[rotor_combo[0]])
                            r2 = Rotor(*rotor_definitions[rotor_combo[1]])
                            r3 = Rotor(*rotor_definitions[rotor_combo[2]])

                            # Создание машины Enigma
                            enigma = Enigma(
                                reflectors[reflector_name],
                                r1,
                                r2,
                                r3,
                                pb,
                                kb
                            )

                            enigma.set_rings((ring1, ring2, ring3))
                            enigma.set_key(pos1 + pos2 + pos3)

                            # Расшифровка
                            decrypted = ''.join(
                                enigma.encipher(letter) if letter.isalpha() else letter
                                for letter in encrypted_message
                            )

                            attempts += 1

                            if known_text.replace(" ", "") in decrypted.replace(" ", ""):
                                time_taken = time.time() - start_time
                                return render(request, 'encrypting/decrypt.html', {
                                    'form': form,
                                    'result': {
                                        'rotors': f"{rotor_combo[0]}-{rotor_combo[1]}-{rotor_combo[2]}",
                                        'reflector': reflector_name,
                                        'positions': f"{pos1}-{pos2}-{pos3}",
                                        'ring_settings': f"{ring1}-{ring2}-{ring3}",
                                        'decrypted_message': decrypted,
                                        'attempts': attempts,
                                        'time_taken': round(time_taken, 2)
                                    }
                                })

                        if attempts >= max_attempts:
                            break
                    if attempts >= max_attempts:
                        break
                if attempts >= max_attempts:
                    break

            # Ничего не найдено
            time_taken = time.time() - start_time
            return render(request, 'encrypting/decrypt.html', {
                'form': form,
                'result': {
                    'error': 'Не удалось найти подходящие настройки',
                    'attempts': attempts,
                    'time_taken': round(time_taken, 2)
                }
            })
    else:
        form = DecryptForm()

    return render(request, 'encrypting/decrypt.html', {'form': form})


def hash_view(request):
    """Представление для страницы хеширования."""
    return render(request, 'encrypting/hash.html')


def hash_text(request):
    """Обработка запроса на хеширование текста."""
    if request.method == 'POST':
        text = request.POST.get('text', '')
        hash_result = hex(simple_hash(text))
        return render(request, 'encrypting/hash.html', {'hash_result': hash_result})
    return redirect('hash_view')


def find_collision_view(request):
    """Обработка запроса на поиск коллизии."""
    if request.method == 'POST':
        try:
            target_hash = int(request.POST.get('target_hash', ''), 16)  # Хеш в hex
            max_length = int(request.POST.get('max_length', 4))
            max_length = min(max_length, 8)

            collisions = find_collision(target_hash, max_length)

            context = {
                'collisions': collisions,
                'target_hash': hex(target_hash),
            }
            return render(request, 'encrypting/hash.html', context)

        except ValueError:
            messages.error(request, 'Неверный формат хеша. Используйте шестнадцатеричное число.')
            return redirect('hash_view')
    return redirect('hash_view')