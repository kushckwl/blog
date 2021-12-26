from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view(),name='home'),
    path('<int:pk>/', views.Detail.as_view(),name='detail'),
    path('create/', views.Create.as_view(),name='create'),
    path('<int:pk>/update', views.Update.as_view(),name='update'),
    path('<int:pk>/delete', views.Delete.as_view(),name='delete'),
     path('user/<str:username>', views.UserPosts.as_view(),name='user-posts'),
    path('signup/', views.signup,name='signup'),
    path('profile/', views.profile,name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),

]
