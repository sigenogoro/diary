from django import forms
from django.contrib.admin.widgets import AdminDateWidget



CHOICE = [
    (0, '高'),
    (1, '中'),
    (2, '低')
]
# 現在は使っていない
class DateForm(forms.Form):
    date_field = forms.DateField(widget=AdminDateWidget())

class PriorityForm(forms.Form):
    priority = forms.ChoiceField(label='優先度', choices=CHOICE, widget=forms.RadioSelect())




