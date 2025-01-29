from django.urls import include, path
from .views import authView, home
from django.contrib.auth import views as auth_views
from ShibeApp import views


app_name = 'ShibeApp'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home , name = 'home'),
    path('signup/', authView, name='authView'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile' ),
 ]  