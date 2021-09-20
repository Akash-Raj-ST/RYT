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
            data = {
                "p_id": place_obj.p_id,
                "place": place_obj.place_name,
                "link": place_obj.link,
                "image": place_obj.image.url,
                "subject":place_obj.subject,
                "place_type":place_obj.place_type
            }
            # serializer = PlacesSerializer(place_obj)
            # data = {"message": "Successful", "data": serializer.data}
            data = {"message": "Successful", "data": data}
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {"message": "Place not found"}
        data = {"message": "Error"}
        return Response(data, status=sta)


@api_view(["GET", "POST"])
def review(request):
    if request.method == "GET":
        try:
            if request.session['id']:
                logged = True
        except:
            logged = False

        place_id = request.data["p_id"] #place_id from payload

        place_obj = Places.objects.filter(p_id=place_id) 
        if place_obj.exists(): #checking if place exists
            review_objs = Review.objects.filter(p_id=place_id) #Fetching reviws of that place
            all_data = [] #contains details of all reviews
            if review_objs.exists():
                for review in review_objs: #looping through every review

                    #Checking whether the user has liked the review
                    if logged:
                        like_objs = Review_like.objects.filter(r_id=review.r_id)
                        if like_objs.exists():
                            for like_obj in like_objs:
                                if like_obj.u_id.user_id == request.session['id']:
                                    liked = True
                                    break
                                else:
                                    liked = False
                        else:
                            liked = False
                    else:
                        liked = False

                    #Fecthing the tags of review
                    tags = []
                    tag_objs = Review_tag.objects.filter(r_id=review.r_id)
                    if tag_objs.exists():
                        for tag_obj in tag_objs:
                            tags.append(tag_obj.tags)

                    #fetching the images of review
                    images = []
                    img_objs = Review_pic.objects.filter(r_id=review.r_id)
                    if img_objs.exists():
                        for img_obj in img_objs:
                            images.append(img_obj.r_pic.url)
                    #data of a particular review
                    data = { 
                        "r_id": review.r_id,
                        "content": review.content,
                        "likes": review.likes,
                        "p_id": review.p_id.p_id,
                        "u_id": review.u_id.user_id,
                        "r_pic":images,
                        "tags": tags,
                        "liked": liked
                    }
                    all_data.append(data)
                f_data = {"message": "Reviews Fetched Successfully", "data": all_data}
            else:
                msg = "No reviews yet"
                data = {"message": msg, "data": None}
            print(all_data)
            return Response(f_data, status=status.HTTP_202_ACCEPTED)
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
