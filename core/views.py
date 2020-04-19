from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
# from django.views.generic.edit import FormView+
from django.views.generic import ListView, DetailView, View
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
import random
import string

from .forms import (
    ProductForm,
    CheckoutForm,
    CouponForm,
    RefundForm,
)

from .models import (
    Product,
    Category,
    Condition,
    ProductReview,
    ReportProduct,
    OrderItem,
    Order,
    Refund,
    Address,
    Coupon,
)



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def HomeView(request):
    category = Category.objects.all()
    context ={
        'latest'     : Product.objects.all().order_by('-published_date')[:4],
        'products'         : Product.objects.extra(
                                select={'count': 'CAST(visit_count AS INTEGER)'}
                            ).order_by('-count')[:5],
        'specialized'       : Product.objects.all() [:10],
        'category' : category,
        "active_home" : "active",
    }

    return render(request, 'homepage/home.html', context=context)



@login_required
def add_product(request):
    category = Category.objects.all()
    condition = Condition.objects.all()
    context = {
        'category' : category,
        'condition' : condition,
        "active_add" : "active",
    }
    if request.method == 'POST':
        if (request.POST['Title'] and
         request.POST['Author'] and
         request.POST['Category'] and
        request.POST['Description'] and 
        request.POST['Price'] and 
        request.POST['Quantity'] and 
        request.POST['Condition']  and 
        request.FILES['Display_Image'] and
        request.POST['pickup_location'] and
        request.POST['coordinates']
        ):
            selected_name            = request.POST['Title'].strip()
            selected_description     = request.POST['Description'].strip()
            selected_price           = request.POST['Price'].strip()
            selected_author          = request.POST['Author'].strip()
            selected_pickup_location = request.POST['pickup_location'].strip()
            selected_coordinates_code  = request.POST['coordinates'].strip()
            selected_total_quantity  = request.POST['Quantity'].strip()
            selected_product_image   = request.FILES['Display_Image']
            try:
                selected_desc_image1   = request.FILES['Descriptive_Image1']
            except:
                selected_desc_image1    = None
            try:
                selected_desc_image2   = request.FILES['Descriptive_Image2']
            except:
                selected_desc_image2    = None
            try:
                selected_desc_image3   = request.FILES['Descriptive_Image3']
            except:
                selected_desc_image3    = None
            try:
                selected_desc_image4   = request.FILES['Descriptive_Image4']
            except:
                selected_desc_image4    = None
            try:
                selected_desc_image5   = request.FILES['Descriptive_Image5']
            except:
                selected_desc_image5    = None
            selected_user            = request.user
            selected_category        = request.POST['Category']
            selected_condition        = request.POST['Condition']
            product_obj = Product.objects.create(
                title = selected_name, 
                category = Category.objects.get(name=selected_category), 
                condition = Condition.objects.get(name=selected_condition), 
                description = selected_description, 
                price = selected_price, 
                author = selected_author, 
                user = selected_user, 
                total_quantity = selected_total_quantity, 
                remaining_quantity = selected_total_quantity,
                pickup_address = selected_pickup_location,
                google_maps_coordinates = selected_coordinates_code,
                display_image = selected_product_image, 
                dec_image1 = selected_desc_image1,
                dec_image2 = selected_desc_image2,
                dec_image3 = selected_desc_image3,
                dec_image4 = selected_desc_image4,
                dec_image5 = selected_desc_image5,
                )
            
            product_obj.save()
            return redirect('home')
        else:
            return render(request, 'add_product.html', {'error':'please fill all the fields'})
    else:
        return render(request, 'add_product.html', context)


@login_required
def product_edit(request, product_id):
    category = Category.objects.all()
    condition = Condition.objects.all()
    product = get_object_or_404(Product, id=product_id)
    product_user = User.objects.filter(id=product.user.id)
    context = {
        'category' : category,
        'condition' : condition,
        'product' : product,
        "active_add" : "active",
    }
    # print(request.user)
    # print(product_user[0])
    if request.user == product_user[0]:
        if request.method == 'POST':
            if (request.POST['new_price'] and
                request.POST['total_quantity']
                ):
                    new_price            = request.POST['new_price']
                    
                    try:
                        discount_price = request.POST['discount_price']
                    except:
                        discount_price = None

                    total_quantity     = request.POST['total_quantity']
                    remaining_quantity           = request.POST['remaining_quantity']
                    product_obj = Product.objects.filter(id=product_id).update(
                        price = new_price,
                        discount_price = discount_price,
                        total_quantity = total_quantity,
                        remaining_quantity = remaining_quantity,
                    )
                    return redirect('profile-info')
            else:
                messages.info(request, "Fill all the fields.")
                return redirect('profile-info')
        else:
            return render(request,'product_edit.html', context)
    else:
        messages.info(request, "We got you. Stop sneeking around.")
        return redirect("home")

            




def SearchResultsView(request):
    category = Category.objects.all()
    if request.method == 'POST':
        if (request.POST['searchword']):
            query = request.POST['searchword']
            object_lists = Product.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query) | Q(user__username__contains = query)
            )

            page    = request.GET.get('page', 1)
            paginator       = Paginator(object_lists, 9)

            try:
                object_list    = paginator.page(page)
            except PageNotAnInteger:
                object_list    = paginator.page(1)
            except EmptyPage:
                object_list    = paginator.page(paginator.num_pages)

            return render(request, 'homepage/search_result.html', {'products':object_list, 'category' : category})
        else:
            return redirect('/')


def ReviewView(request):
    category = Category.objects.all()
    if request.method == 'POST':
        if (request.POST['Comment'] and 
            request.POST['Rating']):
                selected_product         = Product.objects.filter(id=request.POST['product_id'])
                selected_comment          = request.POST['Comment'].strip()
                selected_rating  = request.POST['Rating']
                selected_user    = request.user
                # selected_product = request.POST['product_id']
                # print(selected_product)

                review_obj       = ProductReview.objects.create(
                    comment = selected_comment,
                    rating  = selected_rating,
                    product = selected_product[0],
                    user    = selected_user,
                )
                review_obj.save()
                # selected_product_image   = request.FILES['Display_Image']

                return redirect('../../product/'+request.POST['product_id'])
        else:
            return redirect('home')


    

def product_report(request, id):
    products = Product.objects.filter(id=id)
    category = Category.objects.all()
    
    context = {
        'category': category,
        'product' : products[0],
    }

    if request.method == 'POST':
        if (request.POST['reason']):
            reason = request.POST['reason']
            users            = request.user
            selected_product         = Product.objects.filter(id=request.POST['product_id'])
            print(selected_product[0])
            report_obj = ReportProduct.objects.create(
                user = users,
                reason = reason,
                product = selected_product[0],
            )
            report_obj.save()
            messages.info(request, "Reported Successfully")
            return redirect('home')
        # else:
        #     return render(request, '/', {'error':'please fill all the fields'})
    else:
        return render(request, 'report_product.html', context)

            

    

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    # shipping_country = form.cleaned_data.get(
                    #     'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, ''' shipping_country ''', shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            # apartment_address=shipping_address2,
                            # country=shipping_country,
                            google_maps_coordinates=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    # billing_country = form.cleaned_data.get(
                    #     'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, ''' billing_country ''', billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            # apartment_address=billing_address2,
                            # country=billing_country,
                            google_maps_coordinates=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

            order_items = order.items.all()
            order_items.update(ordered=True)
            for items in order_items:
                # print(items.item.remaining_quantity)
                # print(items.quantity)
                remaining = items.item.remaining_quantity - items.quantity
                # print(items.item.id)
                product_obj = Product.objects.filter(id=items.item.id).update(
                    remaining_quantity = remaining
                )
                items.save()

            order.ordered = True
            order.ref_code = create_ref_code()
            order.save()


            return redirect('home')

                # payment_option = form.cleaned_data.get('payment_option')

                # if payment_option == 'S':
                #     return redirect('core:payment', payment_option='stripe')
                # elif payment_option == 'P':
                #     return redirect('core:payment', payment_option='paypal')
                # else:
                #     messages.warning(
                #         self.request, "Invalid payment option selected")
                #     return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")


# def ProductDetailView(request, **kwargs):
#     # print(id)
#     print(kwargs.get('slug'))
#     product = get_object_or_404(Product, slug=kwargs.get('slug'))
#     # product = Product.objects.filter(slug=slug)
#     # images = get_object_or_404(Image, pk=product_id)
#     # product = Product.objects.select_related(Images)
#     # product.visit_count = product.visit_count + 1
#     # product.save()
    
#     return render(request, 'product.html', {'product':product})


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = "homepage/product.html"

#     slug_url_kwarg = 'slug'

    # def post(self, request, **kwargs):
    #     my_data = request.POST
    #     context =


def ProductDetailView(request, product_id):
    category = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    reviews  = ProductReview.objects.filter(product=product)
    order_item = OrderItem.objects.filter(item=product, ordered=False)
    stars = 0
    review_no = 0
    one = two = three = four = five = 0
    for review in reviews:
        stars = stars + review.rating
        review_no = review_no + 1
        if review.rating == 5:
            five = five + 1
        elif review.rating == 4:
            four = four + 1
        elif review.rating == 3:
            three = three + 1
        elif review.rating == 2:
            two = two + 1
        else:
            one = one + 1

    # stars = stars/review_no
    # print(four)

    context = {
        'product':product, 
        'order_item': order_item,
        'category' : category, 
        'reviews': reviews,
        'one' : one,
        'two' : two,
        'three' : three,
        'four'  : four,
        'five'  : five,
    }
    
    return render(request, 'homepage/product.html', context)



def profile_product(request, user_id):
    user_filtered   = User.objects.filter(id=user_id)
    products        = Product.objects.filter(user=user_id)
    category = Category.objects.all()
    context = {
        'user':user_filtered[0], 
        'current_user' : request.user,
        'category' : category,
        'products'   : products,
        "active_profile" : "active",
    }
    return render(request, 'profile_product.html', context)



def profile_review(request, user_id):
    user_filtered   = User.objects.filter(id=user_id)
    reviews          = ProductReview.objects.filter(user=user_id)
    category = Category.objects.all()

    context = {
        'user':user_filtered[0], 
        'current_user' : request.user,
        'category' : category,
        'reviews'   : reviews,
        "active_profile" : "active",
    }

    return render(request, 'profile_review.html', context)



def profile_info(request):
    user          = User.objects.filter(id=request.user.id)
    category = Category.objects.all()

    context = {
        'user':user[0], 
        'current_user' : request.user,
        'category' : category,
        "active_profile" : "active",
    }

    return render(request, 'profile_info.html', context)



def profile_orders(request):
    category = Category.objects.all()
    user     = request.user
    order_delivered   = Order.objects.filter(user=user, ordered=True, received=True)
    ordered           = Order.objects.filter(user=user, ordered=True, received=False)

    context = {
        'order_delivered' : order_delivered,
        'ordered'         : ordered,
        'user'            : user,
        'current_user'    : request.user,
        'category'        : category,
        "active_profile"  : "active",
    }
    # print(order_delivered[0].user)
    
    return render(request, 'profile_orders.html', context)



def category_detail(request, pk):
    product        = Product.objects.filter(category=pk)
    category = Category.objects.all()
    page            = request.GET.get('page', 1)

    paginator       = Paginator(product, 9)

    try:
        products  = paginator.page(page)
    except PageNotAnInteger:
        products  = paginator.page(1)
    except EmptyPage:
        products  = paginator.page(paginator.num_pages)

    context = {
        'products': products, 
        'category': category,
        "active_category" : "active",
    }

    return render(request, 'homepage/category_detail.html', context) # in this template, you will have access to category and posts under that category by (category.post_set).



def latest_product(request, order):
    category = Category.objects.all()
    if order == 'asc':
        product     = Product.objects.all().order_by('-published_date') #[:2]
    if order == 'desc':
        product     = Product.objects.all().order_by('published_date') #[:2]

    page            = request.GET.get('page', 1)

    paginator       = Paginator(product, 9)

    try:
        products    = paginator.page(page)
    except PageNotAnInteger:
        products    = paginator.page(1)
    except EmptyPage:
        products    = paginator.page(paginator.num_pages)

    return render(request, 'homepage/latest.html', {'products': products, 'category' : category,})





def trending(request):
    category = Category.objects.all()
    product          = Product.objects.extra(
        select={'count': 'CAST(visit_count AS INTEGER)'}
    ).order_by('-count')
    page            = request.GET.get('page', 1)

    paginator       = Paginator(product, 9)

    try:
        products  = paginator.page(page)
    except PageNotAnInteger:
        products  = paginator.page(1)
    except EmptyPage:
        products  = paginator.page(paginator.num_pages)

    context = {
        'products': products, 
        'category' : category,
        "active_trending" : "active",
    }

    return render(request, 'homepage/trending.html', context)




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            category = Category.objects.all()
            order_item = OrderItem.objects.filter(ordered=False)
            context = {
                'object': order,
                'category' : category,
                "active_cart" : "active",
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


# def review_list(request):
#     review_list     = ProductReview.objects.filter(user=request.user)

#     return render(request, "review_list.html", {'review_list':review_list})




# def review_create(request, pk):
#     #   product = get_object_or_404(Product, pk=pk)
#     #   reviewng=request.POST['rating'],
#     #     comment=request.POST['comment'],
#     #     user=request.user,
#     #     product=product)
#     #   review.save()
#     #   return render(request, 'home.html')
#     review_list     = ProductReview.objects.filter()



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        print(order_item.quantity)
        if order_item.quantity < order_item.item.remaining_quantity:
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("order-summary")
        else:
                messages.info(request, "The Stock of this product is lower than your requiremnt. Sorry for the incovenience.")
                return redirect("home")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")



@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)



def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")



class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")



class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("request-refund")

