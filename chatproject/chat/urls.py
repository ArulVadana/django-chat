from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('room/<str:pk>/<str:room_name>',views.room,name='room'),
    path('create_room/',views.createRoom,name='create-room'),
    path('update_room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete_room/<str:pk>/',views.deleteRoom,name='delete-room'),

    path('login/',views.loginPage,name='login-page'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),

    path('profile/<str:pk>',views.Userprofile,name='profile'),

    path('profile_update/<str:pk>',views.UserprofileUpdate,name='profile-update'),

    path('chat/<str:pk1>/<str:pk2>/<str:room_name>',views.PersonalChatRoom,name='personal-chat'),

    path('video_call/<str:pk>',views.videoCall,name='video-call'),

    path('get_token/',views.getToken,name='get-token'),
    path('get_member/', views.usernameVideocall,name='usernameVideocall'),
    path('delete_member/', views.userdelVideo,name='del-user-video'),

]