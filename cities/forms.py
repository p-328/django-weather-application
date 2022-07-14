from django import forms


class CityForm(forms.Form):
    city = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': True,
        'class': 'input is-primary',
        'name': 'city',
        'label': 'City:'
    }))
    country_or_state = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'input is-primary',
                'name': 'country_or_state',
                'label': 'Country/State:'}))
