from django.shortcuts import render
from .forms import recordFrom, SearchForm
from .models import Document
from django.shortcuts import redirect

# Create your views here.
def index(request):
    searchform = SearchForm(request.GET)
    if searchform.is_valid(): #=>値があるかどうか
        keyword = searchform.cleaned_data['keyword']
        data = Document.objects.filter(related_hash__contains=keyword)
    else:
        searchform = SearchForm()
        data = Document.objects.all().order_by('-day')
    params = {
        'title': '日記一覧',
        'data': data,
        'search': searchform,
    }
    return render(request, 'mydiary/index.html', params)

def detail(request, num):
    data = Document.objects.get(id=num)
    search_data = Document.objects.filter(related_hash__contains=data.related_hash)
    params = {
        'title': 'Record_detail',
        'id': num,
        'data': data,
        'search_data': search_data,
    }
    return render(request, 'mydiary/detail.html', params)

def create(request):
    if request.method == 'POST':
        record_info = recordFrom(request.POST)
        if record_info.is_valid():
            record_info.save()
            return redirect(to='/')
    params = {
        'title': 'Record_info(振り返り)',
        'msg': recordFrom()
    }
    return render(request, 'mydiary/create.html', params)

def edit(request, num):
    data = Document.objects.get(id=num)
    if (request.method == "POST"):
        record_edit = recordFrom(request.POST, instance=data)
        record_edit.save()
        return redirect(to='/')
    params = {
        'title': 'Record_edit',
        'id': num,
        'msg': recordFrom(instance=data)
    }
    return render(request, 'mydiary/edit.html', params)

def delete(request, num):
    del_obj = Document.objects.get(id=num)
    if (request.method == "POST"):
        del_obj.delete()
        return redirect(to='/')
    params = {
        'title': 'Record_edit',
        'id': num,
        'msg': del_obj
    }
    return render(request, 'mydiary/delete.html', params)

