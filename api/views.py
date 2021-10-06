from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import AccountsSerializer, PlacesSerializer, ReviewSerializer, Review_likeSerializer, Review_picSerializer, Review_tagSerializer
from .models import Accounts, Places, Place_map, Review, Review_like, Review_pic, Review_tag

from rest_framework.authtoken.models import Token

def check_auth(request):
    try:
        user_id = request.data['user_id']
        token = request.headers["token"]
    except:
        print("user_id and token needed")
        return False

    error = False
    if not user_id:
        print("Need credentials")
        error = True
    if not token:
        print("token needed")
        error = True

    if not error:
        user_obj = Accounts.objects.filter(user_id=user_id)
        if user_obj.exists():
            r_token = Token.objects.filter(user=user_obj[0])
            if r_token.exists():
                if r_token[0].key == token:
                    return True
                else:
                    print("token doesnt match")
            else:
                print("Token doesnt exist")
        else:
            print("User doesnt exist")
    
    return False

def get_rev_images(r_id):
    images = []
    img_objs = Review_pic.objects.filter(r_id=r_id)
    if img_objs.exists():
        for img_obj in img_objs:
            images.append(img_obj.r_pic.url)
    return images

def get_rev_tags(r_id):
    tags = []
    tag_objs = Review_tag.objects.filter(r_id=r_id)
    if tag_objs.exists():
        for tag_obj in tag_objs:
            tags.append(tag_obj.tags)
    return tags

def is_liked(user_id,r_id):
    liked = False
    like_objs = Review_like.objects.filter(r_id=r_id)
    if like_objs.exists():
        for like_obj in like_objs:
            if like_obj.u_id.user_id == int(user_id):
                liked = True
                break
            else:
                liked = False
    return liked

def get_review_data(user_rev_objs,user_id,liked_rev=False):
    rev_data = []
    for user_rev_obj in user_rev_objs:
        rev_id = user_rev_obj.r_id
        rev_images = get_rev_images(r_id=rev_id)
        rev_tags = get_rev_tags(r_id=rev_id)
        #liked can be skipped for user liked request function call
        if liked_rev:
            liked = True
        else:
            liked = is_liked(user_id=user_id,r_id=rev_id)

        rev = {
            "r_id":rev_id,
            "images":rev_images,
            "tags":rev_tags,
            "liked":liked
        }
        rev_data.append(rev)
    return rev_data
    
@api_view(["POST"])
def login(request):
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        user_obj = Accounts.objects.filter(username=username)
        if user_obj.exists():
            user_obj = Accounts.objects.get(username=username)
            token,created = Token.objects.get_or_create(user=user_obj)
            token_key = token.key
            ret_pass = user_obj.password
            if ret_pass == password:
                user_id = user_obj.user_id
                data = {"message": "Login Successful", "user_id": user_id,"key":token_key}
                return Response(data, status=status.HTTP_202_ACCEPTED)
        data = {"message": "Login Failed"}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        username = request.data['username']
        email = request.data['email']

        error = False
        msgs = []
        if Accounts.objects.filter(username=username).exists():
            msgs.append("Username Taken")
            error = True
        if Accounts.objects.filter(email=email):
            msgs.append("Email already used")
            error = True
        if error:
            data = {"message": msgs}
        else:
            serializer = AccountsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {"message": "Account created Successfully"}
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {"message": "Not Valid"}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def profile(request):
    if check_auth(request):
        #profile
        user_id = request.data["user_id"]
        acc_obj = Accounts.objects.get(user_id=user_id)
        data = {
            "user_id": user_id,
            "user_name":acc_obj.username,
            "dp": acc_obj.dp.url,
        }

        #my reviews
        user_rev_objs = Review.objects.filter(u_id = acc_obj)
        data["my_review"] = get_review_data(user_rev_objs,user_id,liked_rev=False)
        
        #like reviews
        liked_rev_objs = Review_like.objects.filter(u_id = acc_obj)
        user_rev_objs = [x.r_id for x in liked_rev_objs]
        data["liked_review"] = get_review_data(user_rev_objs,user_id,liked_rev=True)
        res_data={"message":"successful","data":data}
        return Response(res_data,status=status.HTTP_202_ACCEPTED)
    res_data={"message":"Failed"}
    return Response(res_data,status=status.HTTP_400_BAD_REQUEST)

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

def get_subplace(place_id):
    sub_places = Place_map.objects.filter(pm_id=place_id)
    sp_all = []
    if sub_places.exists():
        for sub_place in sub_places:
            sub_data = {}
            sp_obj= sub_place.spm_id
            sub_data["p_id"] = sp_obj.p_id
            sub_data["place"] = sp_obj.place_name
            sub_data["image"] = sp_obj.image.url
            sub_data["subject"] = sp_obj.subject
            sub_data["place_type"] = sp_obj.place_type
            sp_all.append(sub_data)
    
        return sp_all
    return None

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

            # get subplaces
            subplaces = get_subplace(place_id)
            data["sub_place"] = subplaces
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
    logged = check_auth(request)
    if request.method == "GET":

        place_id = request.data["p_id"] #place_id from payload

        place_obj = Places.objects.filter(p_id=place_id) 
        if place_obj.exists(): #checking if place exists
            review_objs = Review.objects.filter(p_id=place_id) #Fetching reviws of that place
            all_data = [] #contains details of all reviews
            if review_objs.exists():
                for review in review_objs: #looping through every review

                    #Checking whether the user has liked the review
                    if logged:
                       liked = is_liked(request.data["user_id"],review.r_id)
                    else:
                        liked = False

                    #Fecthing the tags of review
                    tags = get_rev_tags(review.r_id)

                    #fetching the images of review
                    images = get_rev_images(review.r_id)

                    # fetch user_dp
                    if review.u_id.dp:
                        user_dp = review.u_id.dp.url
                    else:
                        user_dp = None
                    #data of a particular review
                    data = { 
                        "r_id": review.r_id,
                        "content": review.content,
                        "likes": review.likes,
                        "p_id": review.p_id.p_id,
                        "u_id": review.u_id.user_id,
                        "username":review.u_id.username,
                        "user_dp":user_dp,
                        "r_pic":images,
                        "tags": tags,
                        "liked": liked
                    }
                    all_data.append(data)
                data = {"message": "Reviews Fetched Successfully", "data": all_data}
            else:
                msg = "No reviews yet"
                data = {"message": msg, "data": None}
            print(all_data)
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            msg = "Place not found"
        return Response({"message": msg}, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == "POST":
        place_obj = Places.objects.filter(p_id=request.data["p_id"])
        msgs = []
        if place_obj.exists():
            if logged:
                #data for review table
                review_data = {
                    "p_id": request.data["p_id"],
                    "u_id": request.data['user_id'],
                    "content": request.data["content"],
                }              
                review_serializer = ReviewSerializer(data=review_data)

                if review_serializer.is_valid():
                    new_review = review_serializer.save()

                    #data for tag table
                    tags = request.data.getlist("tags")
                    tag_serializers = []
                    tag_prob = False
                    for tag in tags:
                        tag_data = {
                            "r_id":new_review.r_id,
                            "tags": tag
                        }
                        tag_serializer = Review_tagSerializer(data=tag_data)
                        if tag_serializer.is_valid():
                            tag_serializers.append(tag_serializer)
                        else:
                            tag_prob = True
                            break
                    if not tag_prob:
                        for tag_serializer in tag_serializers:
                            tag_serializer.save()
                    else:
                        msgs.append("Problem in adding tags")

                    #data for pic table
                    r_pics = request.FILES.getlist("r_pic")
                    pic_serializers = []
                    pic_prob = False
                    for pic in r_pics:
                        pic_data = {
                            "r_id":new_review.r_id,
                            "r_pic": pic
                        }
                        pic_serializer = Review_picSerializer(data=pic_data)
                        if pic_serializer.is_valid():
                            pic_serializers.append(pic_serializer)
                        else:
                            pic_prob = True
                            break
                    if not pic_prob:
                        for pic_serializer in pic_serializers:
                            pic_serializer.save()
                    else:
                        msgs.append("Problem in adding pics")

                    msg = "Review added successfully"
                    if not tag_prob and not pic_prob:
                        data = {
                            "message":msg
                        }
                    else:
                        data = {
                            "message":msgs
                        }
                    return Response(data, status=status.HTTP_202_ACCEPTED)
                else: 
                    msg = "Review Not valid"
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

    token = request.headers["token"]
    username = request.data["username"]
    password = request.data["password"]

    user_obj = Accounts.objects.filter(username=username,password=password)
    if user_obj.exists():
        token_key = Token.objects.filter(user=user_obj[0])
        if token_key.exists():
            if token_key[0].key==token:
                token_key[0].delete()
                msg = "Logged out successful"
            else:
                msg = "Token key wrong"
        else:
            msg = "Not logged in"
    else:
        msg = "user not found"
    return Response(msg, status=status.HTTP_202_ACCEPTED)
