from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    params = {
        'title': 'プロジェクト進行状況',
    }
    return render(request, 'management/index.html', params)