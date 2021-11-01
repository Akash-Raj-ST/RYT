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
    # if not token:
    #     print("token needed")
    #     error = True

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
                print("Token doesnt exist so not logged in")
            return True
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
    like_objs = Review_like.objects.filter(r_id=r_id)
    if like_objs.exists():
        for like_obj in like_objs:
            if like_obj.u_id.user_id == int(user_id):
               return True
    return False

def get_review_data(user_rev_objs,login_user,liked_rev=False):
    rev_data = []
    for user_rev_obj in user_rev_objs:
        rev_id = user_rev_obj.r_id
        rev_images = get_rev_images(r_id=rev_id)
        rev_tags = get_rev_tags(r_id=rev_id)
        
        if login_user==False:
            liked = False
        else:
            liked = is_liked(user_id=login_user,r_id=rev_id)

        #check dp exist
        if user_rev_obj.u_id.dp:
            dp = user_rev_obj.u_id.dp.url
        else:
            dp=None

        rev = {
            "r_id":rev_id,
            "u_id":user_rev_obj.u_id.user_id,
            "username":user_rev_obj.u_id.username,
            "user_dp":dp,
            "verified":user_rev_obj.u_id.verified,
            "content":user_rev_obj.content,
            "r_pic":rev_images,
            "tags":rev_tags,
            "likes": user_rev_obj.likes,
            "date":user_rev_obj.date_uploaded,
            "liked":liked,
            "p_id":user_rev_obj.p_id.p_id
        }
        rev_data.append(rev)
    rev_data.sort(key= lambda x:x["likes"],reverse=True)
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
                data = {"message": "Login Successful", "user_id": user_id,"key":token_key,"dp":user_obj.dp.url}
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
                user_obj = Accounts.objects.get(username=username)
                token,created = Token.objects.get_or_create(user=user_obj)
                token_key = token.key

                if user_obj.dp:
                    dp = user_obj.dp.url
                else:
                    dp = None
                data = {"message": "Account created Successfully", "user_id": user_obj.user_id,"key":token_key,"dp":dp}
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {"message": "Not Valid"}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def profile(request,user_id):
    if check_auth(request):
        #profile
        acc_obj = Accounts.objects.filter(user_id=user_id).first()
        login_user = request.data["user_id"]
        if acc_obj:
            if acc_obj.dp:
                dp = acc_obj.dp.url
            else:
                dp = None
                
            data = {
                "user_name":acc_obj.username,
                "dp": dp,
                "verified":acc_obj.verified,
            }

            #my reviews
            user_rev_objs = Review.objects.filter(u_id = acc_obj)
            data["my_review"] = get_review_data(user_rev_objs,login_user=login_user,liked_rev=False)
            data["tot_reviews"] = user_rev_objs.count()
            #like reviews
            liked_rev_objs = Review_like.objects.filter(u_id = acc_obj)
            user_rev_like_objs = [x.r_id for x in liked_rev_objs]
            data["liked_review"] = get_review_data(user_rev_like_objs,login_user=login_user,liked_rev=True)
            data["tot_likes"] = 0
            #total likes user got
            for user_rev_obj in user_rev_objs:
                data["tot_likes"] += user_rev_obj.likes
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
            sub_data["description"] = sp_obj.description
            sub_data["place_type"] = sp_obj.place_type

            place_revs =  Review.objects.filter(p_id = sp_obj.p_id)
            sub_data["reviews"] =place_revs.count()
            sub_data["likes"] = 0
            for place_rev in place_revs:
                sub_data["likes"] += place_rev.likes
            print(sub_data)
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
                "description":place_obj.description,
                "place_type":place_obj.place_type
            }

            place_revs =  Review.objects.filter(p_id = place_id)
            data["reviews"] =place_revs.count()
            data["likes"] = 0
            for place_rev in place_revs:
                data["likes"] += place_rev.likes
            # print(data)
            # get subplaces
            subplaces = get_subplace(place_id)
            #add likes and review of subplace to mainplace
            if subplaces:
                for subplace in subplaces:
                    data["reviews"] += subplace["reviews"]
                    data["likes"] += subplace["likes"]
                data["sub_places"] = subplaces
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
        
        place_id = int(request.data["p_id"]) #place_id from payload
        all_place_id = []
        sub_places = Place_map.objects.filter(pm_id=place_id)
        all_place_id = [x.spm_id.p_id for x in sub_places]
        all_place_id.append(place_id)

        all_data = [] #contains details of all reviews
        for place_id in all_place_id:
            place_obj = Places.objects.filter(p_id=place_id) 
            if place_obj.exists(): #checking if place exists
                review_objs = Review.objects.filter(p_id=place_id) #Fetching reviws of that place
                if review_objs.exists():

                    if logged:
                        login_user = request.data["user_id"]
                    else:
                        login_user = False

                    for rev in get_review_data(review_objs, login_user):
                        all_data.append(rev)
                    data = {"message": "Reviews Fetched Successfully", "data": all_data}
                else:
                    msg = "No reviews yet"
                    data = {"message": msg, "data": None}
        all_data.sort(key= lambda x:x["likes"],reverse=True)
        return Response(data, status=status.HTTP_202_ACCEPTED)

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
                    print(tags)
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

@api_view(["POST"])
def like(request,r_id):
    logged = False
    user_id = request.data["user_id"]

    if user_id:
        if Accounts.objects.filter(user_id=user_id).exists():
            logged = True

    if logged:
        u_id = request.data["user_id"]

        review_obj = Review.objects.filter(r_id=r_id).first()
        liked = Review_like.objects.filter(u_id=u_id,r_id=r_id).first()

        if review_obj:
            tot_likes = review_obj.likes

            if liked: #already liked so dislike
                print("Alreay Liked so dislike")
                liked.delete()
                likes = tot_likes - 1
            else:
                print("Not Liked so liking")
                likes = tot_likes + 1
                like_data = {
                    "r_id":r_id,
                    "u_id":u_id
                }
                like_serializer = Review_likeSerializer(data=like_data)
                if like_serializer.is_valid():
                    like_serializer.save()
                    
            review_obj.likes = likes
            review_obj.save()
            msg = "Success"
            data = {
                "message":msg,
                "likes":likes
            }

            return Response(data,status=status.HTTP_200_OK)
        else:
            msg = "Review does not exist"
    else:
        msg = "login to Like"

    data = {
            "message":msg,
        }
    return Response(data,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def logout(request):

    token = request.headers["token"]

    token_key = Token.objects.filter(key=token)
    if token_key.exists():
        token_key[0].delete()
        msg = "Logged out successful"     
    else:
        msg = "Token not found"

    return Response(msg, status=status.HTTP_202_ACCEPTED)
