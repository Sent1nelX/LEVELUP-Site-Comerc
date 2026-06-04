from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('card', 'Оплата картой'),
        ('cash', 'Оплата при получении'),
    ]
    
    full_name = forms.CharField(max_length=120, label="ФИО")
    phone = forms.CharField(max_length=32, label="Телефон")
    email = forms.EmailField(required=False, label="Email")
    city = forms.CharField(max_length=120, label="Город")
    address = forms.CharField(max_length=220, label="Адрес")
    comment = forms.CharField(required=False, widget=forms.Textarea, label="Комментарий")
    
    # Поля для оплаты
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label="Способ оплаты",
        widget=forms.RadioSelect
    )
    
    # Поля для оплаты по карте (необязательные)
    card_number = forms.CharField(
        max_length=19,
        required=False,
        label="Номер карты",
        widget=forms.TextInput(attrs={'placeholder': '0000 0000 0000 0000'})
    )
    card_holder = forms.CharField(
        max_length=120,
        required=False,
        label="Владелец карты",
        widget=forms.TextInput(attrs={'placeholder': 'JOHN DOE'})
    )
    card_expiry = forms.CharField(
        max_length=5,
        required=False,
        label="Срок действия (MM/YY)",
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'})
    )
    card_cvv = forms.CharField(
        max_length=4,
        required=False,
        label="CVV код",
        widget=forms.PasswordInput(attrs={'placeholder': '123'})
    )


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label="Имя")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=32, required=False, label="Телефон")
    topic = forms.CharField(max_length=180, label="Тема")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")
