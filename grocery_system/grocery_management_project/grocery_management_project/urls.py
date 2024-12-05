"""
URL configuration for grocery_management_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from grocery_app import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from grocery_app.views import SignupPage,LoginPage,HomePage,AboutPage,Add_Product,LogoutPage,ReadProduct,ProductDetails,ProductSearch,AddCart,CartView,DeleteCartItem,Profile,EditProfile,Delete,OrderView,Order1,Payment_success,PaymentModule,payment_cancel,Order_List


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('grocery_app.urls'))
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

