
from django.urls import path
from ecomapp import views

app_name='shop'

urlpatterns = [
    path('',views.allProdCat, name='allProdCat'),
    path('search/', views.allProdSer, name='search_products'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('delete/<int:product_id>/', views.delete_cart, name='delete_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('<slug:c_slug>/',views.allProdCat, name='products_by_category'),
    path('<slug:c_slug>/<slug:p_slug>/', views.allProdDet, name='product_category_details'),

]
