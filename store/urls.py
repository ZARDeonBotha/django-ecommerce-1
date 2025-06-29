
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, ProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/review/', views.submit_review,
         name='submit_review'),
    path('manage-store/', views.manage_store, name='manage_store'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart,
         name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity,
         name='update_cart_quantity'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('store/create/', views.create_store, name='create_store'),
    path('login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('products/', views.all_products, name='all_products'),
    path('orders/', views.order_history, name='order_history'),
    path('store/<int:store_id>/product/create/', views.create_product,
         name='create_product'),
    path('svendor-stores/', views.vendor_store_list,
         name='vendor_store_list'),
    path('vendor-orders/', views.vendor_orders, name='vendor_orders'),
    path('store/<int:store_id>/products/', views.vendor_product_list,
         name='vendor_product_list'),
    path('product/<int:product_id>/', views.product_detail,
         name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart,
         name='add_to_cart')

]
