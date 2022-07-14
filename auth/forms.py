from django import forms


class AuthForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'input is-primary',
        'required': True,
        'name': 'username'
    }))
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input is-primary',
                'required': True,
                'name': 'password'}))


class CreateForm(forms.Form):
    new_username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'input is-primary',
                'name': 'new_username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'required': True,
        'class': 'input is-primary',
        'name': 'email'
    }))
    new_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                'required': True,
                'class': 'input is-primary',
                'name': 'new_password'}))
