from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import json
import requests

import cairosvg
from PIL import Image 
import io,os,sys
from django.core.files.uploadedfile import InMemoryUploadedFile
import mimetypes

def media_to_file(file_object, name):
    if isinstance(file_object, str):
        file_object = io.BytesIO(file_object)

    def getsize(f):
        f.seek(0)
        f.read()
        s = f.tell()
        f.seek(0)
        return s

    name = name.strip()
    content_type, charset = mimetypes.guess_type(name)
    size = getsize(file_object)
    return InMemoryUploadedFile(file=file_object, name=name,
                                field_name=None, content_type="image/jpg",
                                charset=charset, size=size) 
# Create your views here.
def check_session(request):
    if "token" not in request.session or "user_id" not in request.session or "dp" not in request.session:
        return False
    return True

def request_api_files(sub_url, payload=None, files=[], method="POST",token=None):
    url = "http://127.0.0.1:8000/api/"+sub_url

    headers = {
        "Accept": "*/*",
        "token":token,
    }

    response = requests.request(method, url,headers=headers, data=payload,files=files)

    return response

def request_api(sub_url, payload=None,method="POST",token=None):
    url = "http://127.0.0.1:8000/api/"+sub_url
    headers = {'Content-Type': 'application/json','token':token}

    response = requests.request(method, url, headers=headers, data=payload)

    return response

def login(request):
    if request.method == 'GET':
        if not check_session(request):
            return render(request, "login.html")
        return redirect(home)

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        payload = json.dumps({
            "username": username,
            "password": password
        })
        
        response = request_api("login",payload)
        response_json = json.loads(response.text)
        if response.ok:
            request.session["token"] = response_json["key"]
            request.session["user_id"] = response_json["user_id"]
            request.session["dp"] = response_json["dp"]
            messages.success(request, response_json['message'])
            return redirect(home)
        else:
            messages.error(request, response_json['message'])
        
        return render(request, "login.html")

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        payload = {
                "name" : name,
                "username": username,
                "email": email,
                "password": password
        }

        files = None
        dp_file = request.FILES.get('dp_file')
        if not dp_file:
            url = request.POST.get('dp_url')
            out = io.BytesIO()
            cairosvg.svg2png(url=url, write_to=out)
            dp_file = media_to_file(out, "profile.png")
            
        files ={
            "dp":dp_file
        }
        
        response = request_api_files("register", payload,files=files,method="POST")
        response_json = json.loads(response.text)
        if response.ok:
            request.session["token"] = response_json["key"]
            request.session["user_id"] = response_json["user_id"]
            request.session["dp"] = response_json["dp"]
            messages.success(request, response_json['message'])
            return redirect(home)
        else:
            for warning_msg in response_json["message"]:
                messages.warning(request, warning_msg)
            return render(request,"register.html")
        # return HttpResponse("ok")

    elif request.method == "GET":
        return render(request,"register.html")

def profile(request,user_id):
    if not check_session(request):
        return render(request, "login.html")
    payload = json.dumps(
        {
            "user_id": request.session["user_id"],
        }
    )
    response = request_api(f"profile/{user_id}",payload,method="GET",token=request.session["token"])
    response_json = json.loads(response.text)

    if response.ok:
        return render(request,"profile.html",{"data":response_json["data"],"user_id":request.session["user_id"] })
    else:
        return redirect("login")

def home(request):
    if not check_session(request):
        return render(request, "login.html")
    if request.method == "GET":
        response = request_api("home",method="GET",token=request.session["token"])
        response_json = json.loads(response.text)
        data = response_json["data"]
        # print()
        # for p_type in data:
        #     print("type: ",p_type)
        #     for place in data[p_type]:
        #         print(place['id'],"\t",place['place_name'],"\t",place["img"])
        # print("--------------------")
        return render(request,"home.html",{"data":data,"user_id":request.session["user_id"]})

def place(request,p_id):
    if not check_session(request):
        return render(request, "login.html")
    if request.method == "GET":
        response = request_api(f"places/{p_id}",method="GET",token=request.session["token"])
        response_json = json.loads(response.text)
        place_data = response_json["data"]
        payload = json.dumps({
                "p_id":p_id,
                "user_id":request.session["user_id"]
            })
        response = request_api("review",payload,method="GET",token=request.session["token"])
        if response.ok:
            response_json = json.loads(response.text)
            review_data = response_json["data"]
            return render(request,"place.html",{"place":place_data,"reviews":review_data,"user_id":request.session["user_id"] })
        return HttpResponse("Failed")
    
def add_review(request,p_id):
    if not check_session(request):
        request.warning(request,"Login to add Review")
        return render(request, "login.html")

    if request.method == "POST":
        payload ={
            "p_id":p_id,
            "content":request.POST.get("content"),
            "user_id":request.session["user_id"]
        }

        all_tags = request.POST.get("tags")
        tags = all_tags.split(" ")
        payload["tags"] = [x[1:] for x in tags]

        pics = request.FILES.getlist("images")
        pic_files = []
        for pic in pics:
            pic_files.append(("r_pic",pic))
        # print(payload)
        response = request_api_files("review",payload=payload,files=pic_files,method="POST",token=request.session["token"])
        response_json = json.loads(response.text)
        if response.ok:
            messages.success(request,response_json["message"])
            return redirect(f"/places/{p_id}/")
        else:
            messages.warning(request,response_json["message"])
            return HttpResponse("Failed adding review ")  

def logout(request):

    try:
        del request.session["token"]
        del request.session["user_id"]
        del request.session["dp"]
        print("Logged out successfully")
        messages.success(request,"Logged out successfully")
    except:
        print("Not logged in")
        messages.error(request,"Not logged in")

    return redirect("login")