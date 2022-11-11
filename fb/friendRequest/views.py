from django.http import HttpResponse
from django.shortcuts import render
from users.models import Profile, User
from .models import FriendRequests
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="users:site-login")
def friends(request):

    user_profile = Profile.objects.filter(user=request.user).values()[0]
    user_region = ""
    if user_profile['region'] is not None:
        user_region += (user_profile['region']).lower()
    probable_friends = Profile.objects.filter(region=user_region).exclude(user=request.user)
    print((probable_friends))
    print(user_region)
    if len(probable_friends) > 0:
        pass
    else:
        probable_friends = Profile.objects.filter(~Q(user=request.user))
        # anywho = Profile.objects.filter(~Q(user=request.user))
    
    
    
        
    context = {
        "username":request.user, 
        "probable_friends": probable_friends,
        
    }
    return render(request, 'friendRequest/index.html', context)

@login_required(login_url="users:site-login")
def allfriends(request):

    all_req = FriendRequests.objects.filter(Q(user_one=request.user.id) | Q(user_two=request.user.id)).values()
    # print(all_req)
    all_friends = []
    for x in all_req:
        if x['friends'] == True:
            print("x")
            if request.user.id == int(x['user_one']):
                all_friends.append(Profile.objects.get(user_id=int(x['user_two'])))
            elif request.user.id == int(x['user_two']):
                all_friends.append(Profile.objects.get(user_id=int(x['user_one'])))
                
    context = {
        "username":request.user, 
        "all_friends": all_friends,
    }
    return render(request, 'friendRequest/friends.html', context)

def process_friend(request):
    data = json.loads(request.body)
    print(data)
    print(request.user.id)
    FriendRequests.objects.create(
        user_one=request.user.id,
        user_two=data['friend_detail']['friend_id']
    )
    return HttpResponse(200)

def process_friendreq(request):
    data = json.loads(request.body)
    print(data)
    status = data['request_detail']['action']
    friend_id = int(data['request_detail']['req_id'])
    request_1 = FriendRequests.objects.filter(Q(user_one=friend_id) or Q(user_two=friend_id)).values('id')[0]['id']
    request_s = FriendRequests.objects.get(id=int(request_1))
    print(request_s, "yyyyyyy")
    if status == 'decline':
        request_s.state = 'declined'
        request_s.friends = False
        
    elif status == 'accept':
        request_s.state = 'accepted'
        request_s.friends = True
    request_s.save()
        

    return HttpResponse(200)

@login_required(login_url="users:site-login")
def friendsRequest(request):

    
    f_requests = FriendRequests.objects.filter(user_two=request.user.id).values()
    unconfirmed_request = []
    for req in f_requests:
        if req['friends'] is not True and req['state'] != 'declined' and req['state'] != 'accepted':
            rq_sender = Profile.objects.filter(user_id=req['user_one'])[0]
            unconfirmed_request.append(rq_sender)

    print(f_requests)
    print(unconfirmed_request)
    
  
    
        
    context = {
        "friend_requests": unconfirmed_request,
    }
    return render(request, 'friendRequest/requests.html', context)
