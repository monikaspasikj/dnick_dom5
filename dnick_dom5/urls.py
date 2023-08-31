"""dnick_dom5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from dom.views import custom_login, custom_register, confirmation, public_home, user_home, admin_home, \
    product_list_admin, product_list_user, product_list_public, delete_product, about_us_public, about_us_user, \
    about_us_admin, product_details_user, add_product, edit_product, product_details_public, shopping_cart, \
    remove_cart_item, update_cart_item_quantity, custom_logout, create_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public_home, name='public_home'),
    path('login/', custom_login, name='custom_login'),
    path('register/', custom_register, name='custom_register'),
    path('confirmation/', confirmation, name='confirmation'),
    path('admin_home/', admin_home, name='admin_home'),
    path('products_admin/', product_list_admin, name='product_list_admin'),
    path('user_home/', user_home, name='user_home'),
    path('public_home/', public_home, name='public_home'),
    # path('delete_product', delete_product, name='delete_product'),
    path('delete_product/<str:kod>/', delete_product, name='delete_product'),
    path('product_user/<str:kod>/', product_details_user, name='product_details_user'),
    path('product_details_public/<str:kod>/', product_details_public, name='product_details_public'),
    path('products_user/', product_list_user, name='product_list_user'),
    path('products_public/', product_list_public, name='product_list_public'),
    path('aboutus_public/', about_us_public, name='about_us_public'),
    path('aboutus_user/', about_us_user, name='about_us_user'),
    path('aboutus_admin/', about_us_admin, name='about_us_admin'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<str:kod>/', edit_product, name='edit_product'),
    path('shopping_cart/', shopping_cart, name='shopping_cart'),
path('update_cart_item_quantity/', update_cart_item_quantity, name='update_cart_item_quantity'),
    path('remove_cart_item/', remove_cart_item, name='remove_cart_item'),
path('custom_logout/', custom_logout, name='custom_logout'),
path('create_order/<str:product_kod>/', create_order, name='create_order'),


]
              # + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)