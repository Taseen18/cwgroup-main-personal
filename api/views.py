from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from .forms import SignupForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Hobby, User, Friends, FriendRequest
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import django.core.exceptions
from datetime import date
from django.core.paginator import Paginator
from django.db import transaction



def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def signup(request: HttpRequest) -> HttpResponse:
    '''Makes a new user account'''
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = SignupForm()

    return render(request, 'api/registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'api/registration/login.html'
        
@login_required
def spa_view(request: HttpRequest) -> HttpResponse:
    context = {}
    context.update(csrf(request))
    return render(request, 'api/spa/index.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'api/registration/password_change.html'
    
    def get_success_url(self) -> str :
        return '/'

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request: HttpRequest) -> Response:
    '''All profile interactions handled here'''
    user = request.user

    if request.method == 'GET':
        return Response({
            "id": user.id,
            "name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "date_of_birth": user.date_of_birth,
            "hobbies": list(user.hobbies.values('id', 'name')),
        })

    elif request.method == 'PUT':
        data = request.data
        user.first_name = data.get('name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)  # Update last name
        user.username = data.get('username', user.username) 
        user.email = data.get('email', user.email)
        new_dob = data.get('date_of_birth')  # Could be "", valid string, or None
        if new_dob not in (None, ""):
            try:
                user.date_of_birth = new_dob
            except django.core.exceptions.ValidationError:
                print("Invalid DOB")
                pass
        if 'hobbies' in data:
            print("Hobbies received from frontend:", data['hobbies'])  # Debug: print received hobbies
            user.hobbies.set(data['hobbies'])
        user.save()
        return Response({"message": "Profile updated successfully"})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def hobbies_view(request: HttpRequest) -> Response:
    '''Hobbies functions handled here'''
    if request.method == 'GET':
        hobbies = Hobby.objects.all()
        return Response(list(hobbies.values('id', 'name')))

    elif request.method == 'POST':
        data = request.data
        hobby, created = Hobby.objects.get_or_create(name=data['name'])
        return Response({"id": hobby.id, "name": hobby.name, "created": created})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_common_hobbies(request) -> Response:
    '''Gets the users with common hobbies'''
    user_id = request.GET.get("userId")
    user = User.objects.get(id=user_id)


    user_hobbies = user.hobbies.values('id', 'name')

    today_year = date.today().year
    min_age = int(request.GET.get("min_age", 0))
    max_age = int(request.GET.get("max_age", 100))
    min_birth_year = today_year - max_age
    max_birth_year = today_year - min_age

    filtered_users = User.objects.exclude(id=user_id).filter(
        date_of_birth__year__range=(min_birth_year, max_birth_year)
    )

    results = []
    for other_user in filtered_users:
        other_user_hobbies = other_user.hobbies.values('id', 'name')

        common_hobbies = [
            hobby for hobby in user_hobbies if any(
                hobby['id'] == other_hobby['id'] for other_hobby in other_user_hobbies
            )
        ]

        if common_hobbies:
            results.append({
                "user_id": other_user.id,
                "username": other_user.username,
                "common_hobbies_count": len(common_hobbies)
            })

    # Sort by the number of common hobbies (descending)
    results.sort(key=lambda x: x["common_hobbies_count"], reverse=True)

    # Paginate the results
    page = int(request.GET.get("page", 1))
    paginator = Paginator(results, 10)
    page_obj = paginator.get_page(page)

    return Response({
        "userId": user_id,
        "results": list(page_obj),
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
    })

def pagination(dict, page, hobbies_per_page) -> dict:
    '''Paginates a dictionary for the hobbies'''
    paginator = Paginator(dict, hobbies_per_page)
    page_obj = paginator.get_page(page)

    return {"hobbies" : list(page_obj), "page_number" : page_obj.number, "total_pages" : paginator.num_pages}

#Friends format

def format_friend_request(friend_request) -> dict:
    '''Formats a friend request'''
    return {
        "id": friend_request.id,
        "sender": friend_request.sender.username,
        "receiver": friend_request.receiver.username,
        "status": friend_request.status,
    }

def format_friend(friend) -> dict:
    '''Formats a friend relationship'''
    return {
        "id": friend.id,
        "user1": friend.user1.username,
        "user2": friend.user2.username,
    }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def incoming_requests_view(request) -> Response:
    '''Gets incoming friend requests'''
    user = request.user
    incoming_requests = FriendRequest.objects.filter(receiver=user, status='pending')

    formatted_incoming = []
    for request in incoming_requests:
        formatted_request = format_friend_request(request)
        formatted_incoming.append(formatted_request)

    return Response({"incoming_requests": formatted_incoming})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def outgoing_requests_view(request) -> Response:
    '''Gets outgoing friend requests'''
    user = request.user
    outgoing_requests = FriendRequest.objects.filter(sender=user, status='pending')

    formatted_outgoing = []
    for request in outgoing_requests:
        formatted_request = format_friend_request(request)
        formatted_outgoing.append(formatted_request)

    return Response({"outgoing_requests": formatted_outgoing})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request) -> Response:
    '''sends a friend request'''
    sender = request.user
    receiver_username = request.data.get("receiver_username")
    receiver = User.objects.get(username=receiver_username)

    # Check if friend request already exists
    if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
        return Response({"error": "Friend request already exists"})

    friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver, status="pending")

    formatted_request = format_friend_request(friend_request)

    return Response({"message": "Friend request sent successfully", "request": formatted_request})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request) -> Response:
    '''accepts a friend request'''
    request_id = request.data.get("request_id")

    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.status = "accepted"
    friend_request.save()

    new_friendship = Friends.objects.create(user1=friend_request.sender, user2=friend_request.receiver)

    formatted_friendship = format_friend(new_friendship)

    return Response({"message": "Friend request accepted", "friendship": formatted_friendship})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request) -> Response:
    '''rejects a friend request'''
    request_id = request.data.get("request_id")
    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.delete()

    return Response({"message": "Friend request rejected and deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friends_list_view(request) -> Response:
    '''gets all friends'''
    user = request.user
    friendships = Friends.objects.filter(user1=user) | Friends.objects.filter(user2=user)

    formatted_friends = []
    for friendship in friendships:
        formatted_friendship = format_friend(friendship)
        formatted_friends.append(formatted_friendship)

    return Response({"friends": formatted_friends})
