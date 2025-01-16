"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.http import HttpResponse

from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    #path('', main_spa),
    path('', spa_view, name='spa'),

    # Authentication
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),

    # API Endpoints
    path('profile/', profile_view, name='profile'),
    path('hobbies/', hobbies_view, name='hobbies'),
    path('common-hobbies/', user_common_hobbies, name='common-hobbies'),

    # Friends
    path('send-friend-request/', send_friend_request, name='send-friend-request'),
    path('incoming-requests/', incoming_requests_view, name='incoming-requests'),
    path('outgoing-requests/', outgoing_requests_view, name='outgoing-requests'),
    path('accept-friend-request/', accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/', reject_friend_request, name='reject-friend-request'),
    path('friends/', friends_list_view, name='friends-list'),

]
