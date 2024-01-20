
from app1.models import Product, Vendor, CartOrder, Category, CartOrderItems, ProductImages, ProductReview, Wishlist,Address

from taggit.models import Tag
from django.contrib import messages
from django.db.models import Min,Max
def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    products = Product.objects.all()
    all_tags = Tag.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    
    except:
        messages.warning(request,"Please Login First")
        wishlist = 0



    try:
        address= Address.objects.get( user = request.user)
    except:
        address = None
    return {
        'categories':categories,
        'wishlist':wishlist,

        'vendors': vendors,
        'address' : address,
        'products' : products,
        'all_tags' : all_tags,
        'min_max_price': min_max_price,
    }