
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings

from .views import (
    add_product,
    HomeView, 
    category_detail,
    latest_product,
    trending,
    # product,
    ProductDetailView,
    # review,

    profile_product,
    profile_review,
    profile_info,
    profile_orders,
    product_edit,

    
    remove_from_cart,
    remove_single_item_from_cart,
    add_to_cart,


    OrderSummaryView,
    RequestRefundView,
    AddCouponView,
    CheckoutView,
    SearchResultsView,


    ReviewView,
    product_report,
    # review_list,
    # review_create,
)


urlpatterns = [
    path('', HomeView, name="home"),
    path('search/', SearchResultsView, name='search_result'),
    url(r'^latest_product/(?P<order>[\w\-]+)/$', latest_product, name='latest_product'),
    path('trending/', trending, name='trending'),
    url(r'^category/(?P<pk>\d+)/$', category_detail, name='category_detail'),


    # url(r'product/(?P<slug>[^\.]+)/$', ProductDetailView, name='product'),
    path('product/<int:product_id>/', ProductDetailView, name='product'),
    path('product/report/<int:id>/', product_report, name='report-product'),
    path('add_product/', add_product, name='add_product'),


    path('profile/<int:user_id>/product/', profile_product, name='profile-product'),
    path('profile/<int:user_id>/review/', profile_review, name='profile-review'),
    path('profile/general-information/', profile_info, name='profile-info'),
    path('profile/orders/', profile_orders, name='profile-orders'),
    path('profile/product/edit/<int:product_id>/', product_edit, name='product-edit'),



    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),


    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),


    # url('<int:product_id>/reviews/create/',
    # 	review,
    # 	name='review_create'),
    # path('review/list/', review_list, name='review-list'),
    url(r'^review/create/', ReviewView, name='review'),
]



