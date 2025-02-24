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
    path('products/',views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_details'),
    path('add_debtor/', views.add_debtor, name='add_debtor'),
    path('list_debtors/', views.list_debtors, name='list_debtors'),
 ] 