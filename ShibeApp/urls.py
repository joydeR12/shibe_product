from django.urls import include, path
from .views import authView
from django.contrib.auth import views as auth_views
from ShibeApp import views

app_name = 'ShibeApp'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home_combined, name='home'),

    path('signup/', authView, name='authView'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile' ),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='changepass.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='successpass.html'), name='password_change_done'),
    path('products/',views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('save_debtor/', views.save_debtor_order, name='save_debtor_order'),
    path('add_debtor/', views.save_debtor_order, name='add_debtor'),
    path('add_indv/<int:debtor_id>/', views.add_indv, name='add_indv'),
    path('list_debtors/', views.list_debtors, name='list_debtors'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/update/<int:pk>/', views.update_product, name='update_product'),
    path('manage-roles/', views.manage_roles, name='manage_roles'),
    path('debtors/delete/<int:pk>/', views.delete_debtor, name='delete_debtor'),
    path('fetch-product-data/', views.fetch_product_data, name='fetch_product_data'),
    path('debtors/<int:debtor_id>/history/', views.debtor_history, name='debtor_history'),
    path('update-payment/<int:order_id>/', views.update_payment, name='update_payment'),
    path('debtors/update/<int:order_id>/', views.update_debt, name='update_debt'),
    path('api/borrowed-products-chart/', views.borrowed_products_chart_data, name='borrowed-products-chart'),

]

