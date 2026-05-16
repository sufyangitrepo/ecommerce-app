from django.urls import path
from store import views

urlpatterns = [
    path(r'',  views.index_view, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:category_id>/products/', views.products, name='products'),
    path('products/', views.search_products, name='search'),
    path('addToCart/<int:id>', views.add_to_cart, name='addToCart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('deleteCartItem/<int:id>', views.delete_cart_item, name='deleteCartItem'),
    path('increment/<int:id>', views.increment, name='increment'),
    path('decrement/<int:id>', views.decrement, name='decrement'),
    

]