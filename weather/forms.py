import requests
from root.settings import APPID_KEY
from django import forms
from .models import City


class CityForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder": "Введите город"
            }
        )
    )

    def save(self):
        City.objects.create(**self.cleaned_data)
    
    def clean(self):
        has_error = False
        city = self.cleaned_data["name"]
        all_city = City.objects.all()
        for c in all_city:
            if c.name == city:
                self.add_error("name", "Город уже присутствует")
                has_error = True
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city},&lang=ru&appid={APPID_KEY}&units=metric"
            ).json()
        if req["cod"] != 200:
            self.add_error("name", "Неверное название города")
            has_error = True
        if not has_error:
            self.save()
        else:
            raise forms.ValidationError("Неверные данные")
