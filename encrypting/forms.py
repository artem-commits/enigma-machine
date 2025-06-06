from django import forms

ROTORS_CHOICES = (
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
)

REFLECTOR_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

LETTER_CHOICES = [(letter, letter) for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']


class EnigmaForm(forms.Form):
    # Rotor selection
    rotor_r1 = forms.ChoiceField(choices=ROTORS_CHOICES, label='R1')
    rotor_r2 = forms.ChoiceField(choices=ROTORS_CHOICES, label='R2')
    rotor_r3 = forms.ChoiceField(choices=ROTORS_CHOICES, label='R3')

    # Reflector selection
    reflector = forms.ChoiceField(choices=REFLECTOR_CHOICES, label='Рефлектор')

    # Initial rotor positions
    position_r1 = forms.ChoiceField(choices=LETTER_CHOICES, label='Начальное положение R1')
    position_r2 = forms.ChoiceField(choices=LETTER_CHOICES, label='Начальное положение R2')
    position_r3 = forms.ChoiceField(choices=LETTER_CHOICES, label='Начальное положение R3')

    # Ring settings
    ring_r1 = forms.ChoiceField(choices=[(i, i) for i in range(1, 27)], label='Сдвиг кольца R1')
    ring_r2 = forms.ChoiceField(choices=[(i, i) for i in range(1, 27)], label='Сдвиг кольца R2')
    ring_r3 = forms.ChoiceField(choices=[(i, i) for i in range(1, 27)], label='Сдвиг кольца R3')

    # Plugboard settings (up to 10 pairs)
    plugboard_pairs = forms.CharField(
        max_length=100,
        required=False,
        label='Коммутационная панель (пары букв через пробел, например: AB CD EF)',
        help_text='Введите пары букв через пробел (максимум 10 пар)'
    )

    # Message
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Сообщение',
        help_text='Введите текст для шифрования/дешифрования'
    )

class DecryptForm(forms.Form):
    encrypted_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Введите зашифрованное сообщение'
        }),
        label='Зашифрованное сообщение'
    )
    
    known_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: HELLO'
        }),
        label='Известный текст',
        help_text='Введите часть текста, которая должна быть в расшифрованном сообщении'
    )
    
    max_attempts = forms.IntegerField(
        min_value=1,
        max_value=1000000,
        initial=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        label='Максимальное количество попыток'
    )
    
    reflector = forms.ChoiceField(
        choices=[('', 'Любой')] + list(REFLECTOR_CHOICES),
        required=False,
        label='Рефлектор',
        help_text='Выберите рефлектор (если известен)'
    )
