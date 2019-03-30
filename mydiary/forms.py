from django import forms
from .models import Document

class recordFrom(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content','related_hash', 'day']

class SearchForm(forms.Form):
    keyword = forms.CharField(label = '検索', max_length=100)