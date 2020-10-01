from django import forms

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': '1234 Main St'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'email'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'phone'
    }))
    postcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'postcode',
        "value": "3360031",
        "id": "postcode"
    }))

    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'state',
        "id": "state"
    }))
    town = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'town',
        "id": "town"
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'street',
        "id": "street"
    }))
    address_1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'address_1'
    }))
    address_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'sm-form-control',
        'placeholder': 'address_2'
    }))

    # same_billing_address = forms.BooleanField(required=False)
    # save_info = forms.BooleanField(required=False)
    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT)
