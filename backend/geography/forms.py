# geography/forms.py

from django import forms
from leaflet.forms.widgets import LeafletWidget
from .models import GeographicPlace

class GeographicPlaceForm(forms.ModelForm):
    class Meta:
        model = GeographicPlace
        fields = '__all__'
        widgets = {
            'latitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'longitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            # Optionally, you can use LeafletWidget if you decide to switch to GeoDjango's PointField
        }
