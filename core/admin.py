from typing import Set

from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Category,
    Condition,
    Product,
    ProductReview,
    ReportProduct,
    OrderItem,
    Order,
    Coupon,
    Refund,
    Address,
    Comment,
)

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     # readonly_fields = [
#     #     'date_joined',

#     # ]
#     pass

class User(admin.ModelAdmin):
    fields = ('first_name')

class User(admin.ModelAdmin):
    exclude = ('Group')



def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    # 'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        # 'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]



class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        # 'apartment_address',
        'google_maps_coordinates',
        # 'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type']
    search_fields = ['user', 'street_address', 'apartment_address', 'google_maps_coordinates']


class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'reason',
        'is_processed',
    ]
    list_filter = ['is_processed']
    search_fields = ['product']


admin.site.register(Category)
admin.site.register(Condition)
admin.site.register(Product)
# admin.site.register(models.Images)
admin.site.register(ProductReview)
admin.site.register(ReportProduct,ReportAdmin)
admin.site.register(Comment)
# admin.site.register(models.User_Customer)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)