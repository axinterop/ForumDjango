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
from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views as accounts_views
from boards import views as boards_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # boards_views
    path('', boards_views.BoardListView.as_view(), name="home"),
    path('boards/<int:board_id>/', boards_views.TopicListView.as_view(), name="board_topics"),
    path('boards/<int:board_id>/new/', boards_views.new_topic, name="new_topic"),
    path('boards/<int:board_id>/topics/<int:topic_id>/', boards_views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:board_id>/topics/<int:topic_id>/reply/', boards_views.reply_topic, name='reply_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit/',
         boards_views.PostUpdateView.as_view(), name='edit_post'),
    path('boards/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/delete/',
         boards_views.PostDeleteView.as_view(), name='delete_post'),

    # accounts_views
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
    ), name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),
    path('settings/password/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
]
