from django.urls import path
from .views import friends, process_friend, friendsRequest, process_friendreq, allfriends

app_name = 'friend'

urlpatterns = [
    path("", friends, name="friends"),
    path("requests", friendsRequest, name="friendsRequest"),
    path("all_friends", allfriends, name="allfriends"),
    path("process_friend/", process_friend, name="process_friend"),
    path("process_friendreq/", process_friendreq, name="process_friendreq")
   
]