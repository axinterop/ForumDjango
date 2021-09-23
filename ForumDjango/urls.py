"""ForumDjango URL Configuration

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
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from boards import views as boards_views
from accounts import views as accounts_views

urlpatterns = [
    path('', boards_views.home, name="home"),
    path('admin/', admin.site.urls),
    # accounts_views
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # boards_views
    path('boards/<int:board_id>/', boards_views.board_topics, name="board_topics"),
    path('boards/<int:board_id>/new/', boards_views.new_topic, name="new_topic"),
]
