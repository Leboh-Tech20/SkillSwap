from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('post-skill/', views.post_skill, name='post_skill'),
    path('messages/<int:user_id>/', views.message_view, name='messages'),
    path('review/', views.leave_review, name='leave_review'),
    path('matches/', views.match_list, name='matches'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('messages/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('agreements/create/', views.create_agreement, name='create_agreement')





]
