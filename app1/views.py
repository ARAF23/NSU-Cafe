
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import uuid
from .forms import ProfileForm  # Import your custom ProfileForm if you have one
from .models import Coupon
from decimal import Decimal

from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from app1.models import Product, Vendor, CartOrder, Category, CartOrderItems, ProductImages, ProductReview, Wishlist,Address
from .models import Profile, RegistaredProfile
from taggit.models import Tag
from django.db.models import Count, Avg
from app1.forms import ProductReviewForm
from django.http import JsonResponse, Http404
from stripe import Review
from django.core import serializers
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


'''Creating views for signup, login, logout, verification, 
    sending email, verification failure, verification success.
'''
def HomePage(request):
        return render(request,'home.html')

def index(request):
        
        return render(request, 'index.html')

#popular items
def popular(request):

        products = Product.objects.filter(product_status="published", featured=True).order_by("-id") 
        context = {
            "products": products
        }   
        return render(request, 'popular.html',context)

#items
def items(request):
        products = Product.objects.filter(product_status="published").order_by("-id") 
        context = {
            "products": products
        }
        return render(request, 'product-list.html',context)

#categorylist view
def categorylist(request):
        categories = Category.objects.all()
        context = {
            "categories": categories
        }
        return render(request, 'categorylist.html',context)


#category product list view
def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)  # Corrected the category retrieval
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        "category": category,  
        "products": products,
    }
    
    return render(request, "category-product-list.html", context)


#vendor list view
def vendor_list_view(request):
    vendors = Vendor.objects.all()  
    context = {
        'vendors': vendors, 
    }
    return render(request, 'vendor-list.html', context)


#vendor's informations
def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)  
    products = Product.objects.filter(vendor=vendor, product_status="published" )
    context = {
        'vendor': vendor, 
        'products': products, 

    }
    return render(request, 'vendor-detail.html', context)


#item's info
def product_detail_view(request, pid):


    product = Product.objects.get(pid=pid) 
    products = Product.objects.filter(category = product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #avg
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()

    rating_percentage = {
        1: 0,  # Initialize to 0
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

    total_reviews = reviews.count()
    if total_reviews > 0:
        for star in range(1, 6):
            count = reviews.filter(rating=star).count()
            rating_percentage[star] = (count / total_reviews) * 100
    


    p_image = product.p_images.all()
    context = {
        'p': product,
        'p_image': p_image, 
        'products': products,
        'review_form': review_form,
        'average_rating': average_rating,
        'rating_percentage': rating_percentage,  # Pass the rating_percentage dictionary
        'reviews': reviews,

    }
    return render(request, 'product-detail.html', context)


#tags
def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None

    all_tags = Tag.objects.all()


    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag,
        "all_tags": all_tags,  # Add all_tags to the context

    }
    
    return render(request, "tag.html", context)


# review 
def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context={
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse({
    'bool': True,
    'context': context,
    'average_reviews': average_reviews
})


#filter products
def filter_product(request):
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

  
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    data = render_to_string("async/product-list.html", {"products": products})

    return JsonResponse({"data": data})



def cart_view(request):
    cart_total_amount = 0  # Initialize cart_total_amount to 0
    gta = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            gta = cart_total_amount + 10
        
        return render(request, "cart.html", {
            "cart_data": request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,'gta': gta,

            })
    else:
        messages.warning(request, "your cart is empty")
        return redirect("items")



def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    gta = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            gta = cart_total_amount + 10

    context = render_to_string("async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount': cart_total_amount,'gta': gta})
    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})



#update cart
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = str(request.GET['qty'])

    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty 
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    gta = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            gta = cart_total_amount + 10

    context = render_to_string("async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount': cart_total_amount,'gta': gta})
    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})



#checkout

@login_required
def checkout_view(request):

    cart_total_amount = 0
    gta = 0
    total_amount =0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
        order= CartOrder.objects.create(

            user=request.user,
            price = total_amount+10

        )

        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            gta = cart_total_amount + 10

            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),  # INVOICE_NO-5
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )


    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': gta,
        'item_name': 'Order-Item-No-'+str(order.id),
        'invoice': 'INVOICE_NO-'+str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('app1:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('app1:payment-completed')),
        'cancel_url': 'http://{}{}'.format(host, reverse('app1:payment-failed')),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    #cart_total_amount = 0
    #gta = 0

    #if 'cart_data_obj' in request.session:
        #for p_id, item in request.session['cart_data_obj'].items():
            #cart_total_amount += int(item['qty']) * float(item['price'])
            #gta = cart_total_amount + 10
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request,"Select One Address")
        active_address = None

    return render(request, "checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount': cart_total_amount,'gta': gta,'paypal_payment_button':paypal_payment_button,'active_address':active_address})


@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    gta = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            gta = cart_total_amount + 10

    return render(request, "payment-completed.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount': cart_total_amount,'gta': gta})


@login_required
def payment_failed_view(request):
    return render(request, 'payment-failed.html')


@login_required
def customer_dashboard(request):


    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        new_address = Address.objects.create(user=request.user, address=address, mobile=mobile)
        messages.success(request, "Address Added Successfully.")
        return redirect("app1:dashboard")

  
    context = {
        'profile': profile,
        'orders': orders,
        'address': address

    }
    return render(request,"dashboard.html",context)


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        "order_items": order_items,
    }
    return render(request, 'order-detail.html', context)


def make_address_default(request):
    id = request.GET.get('id')
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})





#search
def search_view(request):
    query = request.GET.get("q")
    products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by("-date")
    
    context = {
        "products": products,
        "query": query,
    }
    
    return render(request, "search.html", context)

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})










#signup

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        uni_id = request.POST.get('university_id')  # Get the university ID from the form

        try:
            if pass1 != pass2:
                messages.warning(request, 'Password Mismatch!!')
                return redirect('signup')

            if User.objects.filter(username=uname).exists():
                messages.warning(request, 'Username is taken')
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is taken')
                return redirect('signup')

            # Check the format of the university ID
            if not (uni_id[:3] in {'201', '202', '203', '211', '212', '213', '191', '192', '193', 
            '181', '182', '183', '171', '172', '173', '161', '162', '163', '221', '222', '223'} 
            and uni_id[-3:] in {'042', '642', '025', '625', '643'}):
                messages.warning(request, 'Invalid ID')
                return redirect('signup')
            
            if not (email.endswith('@northsouth.edu')):
                messages.warning(request, 'Please use NSU Email')
                return redirect('signup')


            auth_token = str(uuid.uuid4())
            my_user = User.objects.create_user(username=uname, email=email)
            my_user.set_password(pass1)
            profile_obj = Profile.objects.create(user=my_user, auth_token=auth_token)
            profile_obj.save()
            prof_obj = RegistaredProfile.objects.create(university_id=uni_id)
            prof_obj.save()

            send_mail_after_registration(email, auth_token, uname)
            my_user.save()

            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'signup.html')

#login
def LoginPage(request):
    if request.method=='POST':
        username= request.POST.get('username') # taking user name 
        pass1= request.POST.get('pass') # taking pass
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('items')
        else:
            messages.warning(request, 'username or password is incorrect')

            

    return render(request,'login.html')

















#emailverification defs starts here


def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/success')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
    

def error_page(request):
    return  render(request , 'error.html')
    
def send_mail_after_registration(email , token, uname):
    subject = 'Your account needs to be verified'
    message = f'Hello " {uname} " paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

    #can return if needed

def LogoutPage(request):
    logout(request)
    return redirect('/login')

@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.all()
    context = {
        "w": wishlist
    }
    return render(request, "wishlist.html", context)

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    context = {}
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
    context = {
            "bool": True
    }
    return JsonResponse(context)


# remove wishlist
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    wishlist_d = Wishlist.objects.get(id=pid)
    delete_product = wishlist_d.delete()

    context = {
        "bool": True,
        "wishlist": wishlist
    }

    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string("async/wishlist-list.html", context)
    return JsonResponse({'data':t, 'w': wishlist_json})



def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_sav = form.save(commit=False)
            profile_sav.user = request.user
            profile_sav.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("app1:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context={
        "form": form,
        "profile": profile,

    }


    return render(request, "profile-edit.html", context)

