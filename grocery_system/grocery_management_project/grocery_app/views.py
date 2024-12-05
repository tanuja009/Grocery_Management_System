from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import Product_Add_Form
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
import logging


stripe.api_key = settings.STRIPE_SECRET_KEY

class SignupPage(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        
            uname=request.POST.get('username')
            email=request.POST.get('email')
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')

            if pass1!=pass2:
                return HttpResponse("Your password and confrom password are not Same!!")
            else:

                my_user=User.objects.create_user(uname,email,pass1)
                my_user.save()
            
                return redirect('login')

class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pass')
        if not username or not password:
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.email)
            try:
                send_mail(
                "Welcome Mail",
                "Welcome To Our Grocery World",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
                )
                print("Email sent successfully.")
            except Exception as e:
                return HttpResponse("error")
            return redirect('home')
        else:
           
            return redirect('login')


class HomePage(View):
    def get(self,request):
        products =Product.objects.all()
        data=category.objects.all()
        images = [
        "https://cdn.pixabay.com/photo/2022/08/01/07/59/vegetables-7357585_640.png",
        "https://5.imimg.com/data5/MG/FQ/SA/SELLER-283756/all-fmcg-grocery-products.jpg",
        "https://media.istockphoto.com/id/171302954/photo/groceries.jpg?s=612x612&w=0&k=20&c=D3MmhT5DafwimcYyxCYXqXMxr1W25wZnyUf4PF1RYw8="
        ]
       
        return render(request,"home.html",{'products':products,'categories':data,'images':images})
    

class AboutPage(View):   
    def get(self,request):
        categories=category.objects.all()
        return render(request,"about_us.html",{'categories':categories})
    

class Add_Product(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request):
        form = Product_Add_Form()
        return render(request, 'add.html', {'form':form})
    
    def post(self,request):
            form = Product_Add_Form(request.POST, request.FILES)
            categories=category.objects.all()
            if form.is_valid():
                form.save()
                user=Product.objects.all()
                return render(request,'home.html',{'user':user,'categories':categories})
       

class LogoutPage(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request):
        logout(request)
        return redirect('login')
    
class ReadProduct(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request,id):
        categories=category.objects.get(id=id)
        product=Product.objects.filter(category=categories)
        categories=category.objects.all()
        return render(request,"Readcart.html",{'data':product,'categories':categories})


class ProductDetails(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request, id):
        item = get_object_or_404(Product, id=id)
        categories=category.objects.all()
        return render(request, "details.html", {'item': item,'categories':categories})
    
class ProductSearch(LoginRequiredMixin,View):
    login_url = 'login' 
    def get(self,request):
        query = request.GET.get('q','')
        if query:
            products = Product.objects.filter(product_name__icontains=query)
        else:
            products = Product.objects.all()
        return render(request, 'search.html', {'products': products, 'query': query})
    
class AddCart(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, id):
        user = request.user
        product = get_object_or_404(Product, id=id) 
        print(f"Product: {product}")
        cart_item, created = CartItem.objects.get_or_create(product=product, user=user)

        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        
        cart_item.save() 
        items = CartItem.objects.filter(user=user)
        total_price = sum(item.product.price * item.quantity for item in items)
        return render(request, 'cart.html', {
            'items': items,
            'total_price': total_price
        })

class CartView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            username = request.user
            print(f"Username: {username}")
            items = CartItem.objects.filter(user=username)
            print(f"Items: {items}") 
            categories = category.objects.all()
            shipping_charge = 70
            total_price = sum(item.product.price * item.quantity for item in items)
            print(f"Total Price: {total_price}")
            return render(request, 'cart.html', {
                'items': items,
                'total_price': total_price,
                'categories': categories,
                'shipping_charge': shipping_charge
            })
        except Exception as e:
            logging.error(f"Error in CartView: {e}")
            return HttpResponse(f"Error: {e}")

class DeleteCartItem(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,id):
        username=request.user
        item=CartItem.objects.filter(id=id)
        item.delete()
        items=CartItem.objects.filter(user=username)
        return render(request,'cart.html',{'items': items})           
    
class Profile(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        try:
            user = request.user
            profile = get_object_or_404(User, username=user.username)
            categories=category.objects.all()

            return render(request, 'profile.html', {'profile': profile,'categories':categories})
        except User.DoesNotExist:
            return HttpResponse("Profile not found", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

class EditProfile(LoginRequiredMixin,View):
    login_url = 'login'  
    def get(self, request, id=None):
        user = request.user
        app_user = User.objects.get(username=user)
        return render(request, "edit_profile.html", {"profile": app_user})

    def post(self, request, id):
        username = request.POST.get("username")
        email = request.POST.get("email")
        print("Email is:", email)
        print(username)

        if email:
            update_data = User.objects.filter(email=email).first()
        else:
            update_data = User.objects.filter(id=id).first()

        if update_data:
            print("Update data:", update_data)
            update_data.username = username
            update_data.save()
            print(update_data)
            return redirect("profile")
        else:
            return HttpResponse("Data not found")


class Delete(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return redirect('home')

class OrderView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, id):
        user=request.user
        order = get_object_or_404(Product, id=id)
        categories=category.objects.all()

        print(data)
        return render(request, 'order_confirm.html', {'data': order,'categories':categories})
    
    
class Order1(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, id):
        if isinstance(request.user,AnonymousUser):
            return redirect('login')  

        user = request.user
        product = get_object_or_404(Product, id=id)
        order, is_created = Order.objects.get_or_create(product=product, user=user)
        print(order)
        categories = category.objects.all()

        shipping_charge = 70
        total_price = order.product.price + shipping_charge
        
        return render(request, 'proceed_payment.html', {
            'order': order,
            'total_price': total_price,
            'shipping_charge': shipping_charge,
            'categories': categories
        })
    

class PaymentModule(View):
    def get(self,request):
         return JsonResponse({'error': 'Invalid request method'}, status=405)
    def post(self,request, id):
        user=request.user
        if id != "null":
            order = get_object_or_404(Order, id=id)
            try:
                    product = order.product
                    shipping_charge=70
                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=[{
                            'price_data': {
                                'currency': 'inr',
                                'product_data': {
                                    'name': product.product_name,
                                },
                                'unit_amount': int(product.price * 100)+(shipping_charge*100),
                            },
                            'quantity': 1,
                        }],
                        mode='payment',
                        success_url=request.build_absolute_uri('/payment_success/'),
                        cancel_url=request.build_absolute_uri('/payment_cancel/'),
                    )
                    
                    return redirect(session.url, code=303)
            except stripe.error.StripeError as e:
                    return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=400)
            except Exception as e:
                    return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

        else:
            items = CartItem.objects.filter(user=request.user)
            shipping_charge=70
            if request.method == 'POST':
                try:
                    line_items = []
                    for item in items:
                        product = item.product
                        line_items.append({
                            'price_data': {
                                'currency': 'inr',
                                'product_data': {
                                    'name': product.product_name,
                                },
                                'unit_amount': int(product.price * 100)+(shipping_charge*100) ,
                            },
                            'quantity': item.quantity,
                        })
                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=line_items,
                        mode='payment',
                        success_url=request.build_absolute_uri('/payment_success/'),
                        cancel_url=request.build_absolute_uri('/payment_cancel/'),
                    )
                    return redirect(session.url, code=303)
                except stripe.error.StripeError as e:
                    return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=400)
                except Exception as e:
                    return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
            else:
                return JsonResponse({'error': 'Invalid request method'}, status=405)
        
class Payment_success(View):
   def get(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return render(request, 'error.html', {'message': 'Your cart is empty!'})
        orders = [
            Order(user=user, product=item.product)
            for item in cart_items
        ]
        Order.objects.bulk_create(orders)
        cart_items.delete()
        send_mail(
            "Thank You for Your Order",
            "Thanks for your order and your interest!",
            "tapatidar@bestpeers.com",
            [user.email],
            fail_silently=False,
        )

        return render(request, 'payment_success.html')


class payment_cancel(View):
    def get(self,request):
        return render(request, 'home.html')

class Order_List(View):
    def get(self,request):
        user=request.user
        orders = Order.objects.all().order_by('-created_at')
        return render(request, 'order_list.html', {'orders': orders})


    
