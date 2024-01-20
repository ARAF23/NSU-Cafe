
from django.urls import include, path
from app1.views import add_to_cart, add_to_wishlist, ajax_add_review, cart_view, checkout_view, customer_dashboard, delete_item_from_cart,filter_product, index, category_product_list_view, make_address_default, order_detail, payment_completed_view, payment_failed_view, profile_update, remove_wishlist, search_view,tag_list, product_detail_view, update_cart, vendor_detail_view, vendor_list_view, wishlist_view
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin

app_name = "app1"

urlpatterns = [
  path('', index),

  path('item/<pid>',product_detail_view,name='product-detail'),

  path('category/<cid>/',category_product_list_view,name='catlist'),
  path('vendors/',vendor_list_view,name='vendor-list'),
  path('vendor/<vid>',vendor_detail_view,name='vendor-detail'),
  path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),
  path('search/',search_view,name='search'),
  path('ajax-add-view/<int:pid>/',ajax_add_review,name='ajax-add-view'),

  path('filter-products/',filter_product,name='filter-product'),
    
  path('add-to-cart/',add_to_cart,name='add-to-cart'),
  
  path('cart/',cart_view,name='cart'),
  path('delete-from-cart/',delete_item_from_cart,name='delete-from-cart'),
  path('update-cart/',update_cart,name='update-cart'),

  path('checkout/',checkout_view,name='checkout'),
  
  path('paypal/',include('paypal.standard.ipn.urls')),

    
  path('payment-completed/',payment_completed_view,name='payment-completed'),
  path('payment-failed/',payment_failed_view,name='payment-failed'),
  path('dashboard/',customer_dashboard,name='dashboard'),

  path('dashboard/order/<int:id>',order_detail,name='order-detail'),

  path('make-default-address/',  make_address_default ,name='make-default-address'),
  
  path('wishlist/',  wishlist_view ,name='wishlist'),

  path('add-to-wishlist/',  add_to_wishlist ,name='add-to-wishlist'),
  
  path('remove-from-wishlist/',  remove_wishlist ,name='remove-from-wishlist'),

  path('profile/update/', profile_update ,name='profile-update'),





















    # ... other URL patterns here
]

'''if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) '''