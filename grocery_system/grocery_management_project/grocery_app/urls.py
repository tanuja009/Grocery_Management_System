from django.urls import path
from grocery_app import views
from django.contrib import admin
from django.urls import path,include
from grocery_app import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from grocery_app.views import SignupPage,LoginPage,HomePage,AboutPage,Add_Product,LogoutPage,ReadProduct,ProductDetails,ProductSearch,AddCart,CartView,DeleteCartItem,Profile,EditProfile,Delete,OrderView,Order1,Payment_success,PaymentModule,payment_cancel,Order_List

urlpatterns = [
    path('login/',LoginPage.as_view(),name='login'),
    path('signup/',SignupPage.as_view(),name='signup'),
    path('',HomePage.as_view(),name="home"),
    path('addproduct/',Add_Product.as_view(),name="addproduct"),
    path('about/',AboutPage.as_view(),name="About"),
    path('logout_view/',LogoutPage.as_view(),name="logout_view"),
    path('read_cat/<int:id>/',ReadProduct.as_view(), name="read"),
    path('product_details/<int:id>/',ProductDetails.as_view(), name='product_details'),
    path('Add_cart/<int:id>/',AddCart.as_view(),name="Add_cart"),
    path('search/',ProductSearch.as_view(), name='product_search'),
    path('profile/',Profile.as_view(),name="profile"),
    path('cart_view/',CartView.as_view(),name="cart_view"),
    path('edit_profile/<int:id>/',EditProfile.as_view(),name="edit_profile"),
    path('Delete/<int:id>',Delete.as_view(),name="Delete"),
    path('order_confirm/<int:id>/',OrderView.as_view(),name="order_confirm"),
    path('order/<int:id>/',Order1.as_view(),name="order"),
    path('payment/<slug:id>/',PaymentModule.as_view(), name='payment'),
    path('create-checkout-session/<int:id>/',PaymentModule.as_view(), name='create-checkout-session'),
    path('payment_success/',Payment_success.as_view(), name='payment_success'),
    path('capayment_cancel/',payment_cancel.as_view(), name='payment_cancel'),
    path('orders/',Order_List.as_view(), name='order_list'),
    path('deletecartitem/<int:id>',DeleteCartItem.as_view(),name="deletecartitem")
]