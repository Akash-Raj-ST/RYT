from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import json
import requests

# Create your views here.


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
        return render(request, "login.html")

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        payload = json.dumps({
            "username": username,
            "password": password
        })
        
        response = request_api("login",payload)
        response_json = json.loads(response.text)
        if response.ok:
            request.session["token"] = response_json["key"]
            request.session["user_id"] = response_json["user_id"]
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
        if dp_file:
            files ={
                "dp":dp_file
            }
            print(files)
        
        response = request_api_files("register", payload,files=files,method="POST")
        response_json = json.loads(response.text)
        if response.ok:
            return render(request,"login.html")  
        else:
            return HttpResponse(response_json['message'])

    elif request.method == "GET":
        return render(request,"register.html")

def profile(request,user_id):
    payload = json.dumps(
        {
            "user_id": request.session["user_id"],
        }
    )
    response = request_api(f"profile/{user_id}",payload,method="GET",token=request.session["token"])
    if response.ok:
        response_json = json.loads(response.text)
        return render(request,"profile.html",{"data":response_json["data"],"user_id":request.session["user_id"] })
    else:
        return redirect("login")

def home(request):
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
        print(data)
        return render(request,"home.html",{"data":data,"user_id":request.session["user_id"]})

def place(request,p_id):
    if request.method == "GET":
        response = request_api(f"places/{p_id}",method="GET",token=request.session["token"])
        response_json = json.loads(response.text)
        place_data = response_json["data"]
        print(response_json)
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
    
def add_review(request):
    if request.method == "POST":

        payload ={
            "p_id":request.POST.get("p_id"),
            "content":request.POST.get("content"),
            "tags":request.POST.get("tags"),
            "user_id":request.session["user_id"]
        }
        pics = request.FILES.getlist("images")
        pic_files = []
        for pic in pics:
            pic_files.append(("r_pic",pic))
        print(pic_files)
        response = request_api_files("review",payload=payload,files=pic_files,method="POST")
        if response.ok:
            response_json = json.loads(response.text)
            return HttpResponse(response_json["message"])
        return HttpResponse("Failed adding review")