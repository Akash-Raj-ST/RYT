from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .optimizer import css_parser

def main(request):
    if request.method == "GET":
        return render(request, 'index.html')
    else:
        return render(request, 'data.html')

def upload(request):
    print("upload...")
    if request.method == "POST":
        files = request.FILES.getlist("CSS_files")
        data = []
        for file in files:
            d = handle_uploaded_file(file)
            d["name"] = file.name
            data.append(d)
        
        print(data)
    return render(request, 'result.html',{"data":data})



def handle_uploaded_file(f):
    info = {}
    with open('static/upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    css_p = css_parser('static/upload/'+f.name)
    info['new_file'] = css_p.new_file
    info['old_size'] = css_p.old_size
    info['new_size'] = css_p.new_size
    info['percentage'] = css_p.percentage

    return info
        
    
