from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, PlacesSerializer, ReviewSerializer
from .models import User, Places, Review, Review_like, Review_pic, Review_tag


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        user_name = request.data['user_name']
        password = request.data['password']
        print("from api: ",user_name,password)
        user_obj = User.objects.filter(user_name=user_name)
        if user_obj.exists():
            user_obj = User.objects.get(user_name=user_name)
            ret_pass = user_obj.password
            if ret_pass == password:
                user_id = user_obj.user_id
                request.session["id"] = user_id
                data = {"message": "Login Successful", "user_id": user_id}
                return Response(data, status=status.HTTP_202_ACCEPTED)
        data = {"message": "Login Failed"}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        user_name = request.data['user_name']
        email = request.data['email']

        error = False
        msgs = []
        if User.objects.filter(user_name=user_name).exists():
            msgs.append("Username Taken")
            error = True
        if User.objects.filter(email=email):
            msgs.append("Email already used")
            error = True
        if error:
            data = {"message": msgs}
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {"message": "Account created Successfully"}
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {"message": "Not Valid"}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def all_place_cat(request):
    if request.method == "GET":
        data = {}
        place_obj = Places.objects.all()
        for place in place_obj:
            if(place.place_type in data):
                data[place.place_type].append({"id":place.p_id,"place_name":place.place_name,"img":place.image.url})
            else:
                data[place.place_type] = [{"id":place.p_id,"place_name":place.place_name,"img":place.image.url}]

        data = {"message": "Successful", "data": data}
        return Response(data, status=status.HTTP_202_ACCEPTED)

@api_view(["GET"])
def places(request, place_id):
    if request.method == "GET":
        place_obj = Places.objects.filter(p_id=place_id)
        sta = status.HTTP_401_UNAUTHORIZED
        if place_obj.exists():
            place_obj = Places.objects.get(p_id=place_id)
            # data = {
            #     "p_id": place_obj.p_id,
            #     "place": place_obj.place,
            #     "link": place_obj.link,
            #     "image": place_obj.image.url
            # }
            serializer = PlacesSerializer(place_obj)
            data = {"message": "Successful", "data": serializer.data}
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {"message": "Place not found"}
        data = {"message": "Error"}
        return Response(data, status=sta)


@api_view(["GET", "POST"])
def review(request):
    if request.method == "GET":
        place_id = request.data["p_id"]
        place_obj = Places.objects.filter(p_id=place_id)
        if place_obj.exists():
            review_objs = Review.objects.filter(p_id=place_id)
            if review_objs.exists():
                serializer = ReviewSerializer(review_objs, many=True)
                data = {"message": "Reviews Fetched Successfully", "data": serializer.data}
            else:
                msg = "No reviews yet"
                data = {"message": msg, "data": None}
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            msg = "Place not found"
        return Response({"message": msg}, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == "POST":
        place_obj = Places.objects.filter(p_id=request.data["p_id"])
        if place_obj.exists():
            logged = False
            try:
                if request.session['id']:
                    logged = True
            except:
                logged = False
            if logged:              
                serializer = ReviewSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    msg = "Review added successfully"
                    data = {
                        "message":msg
                    }
                    return Response(data, status=status.HTTP_202_ACCEPTED)
                else: 
                    msg = "Not valid"
            else:
                msg = "Login to add Review"
        else:
            msg = "Place not found"
        data = {
            "message": msg
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def logout(request):
    msg = None
    if request.method == "GET":
        try:
            del request.session["id"]
            msg = {"Logged out"}
        except:
            msg = {"Not logged in"}
    return Response(msg, status=status.HTTP_202_ACCEPTED)
