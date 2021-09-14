  
from django import forms

class ListingForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    img_url = forms.CharField(widget=forms.URLInput())
    bid = forms.CharField(widget=forms.NumberInput())
