from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.conf import settings

import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from django.shortcuts import reverse
from django_countries.fields import CountryField



USER_TYPE_CHOICES = (
        ('CR', 'Customer'),
        ('HR', 'HR'),
        ('RM', 'Report_Manager'),
        ('DB', 'Delivery_Boy'),
        ('CQ', 'Customer_Queries_Replier'),
    )

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('P', 'Pickup'),
    ('S', 'Shipping'),
)



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class HR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Report_Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Queries_Replier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Delivery_Boy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class User_Customer(models.Model):
    
    user_type = models.CharField(
        max_length=10,
        blank=False,
        choices=USER_TYPE_CHOICES,
        default = 'CR'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class User_Company(models.Model):
    
    user_type = models.CharField(
        max_length=10,
        blank=False,
        choices=USER_TYPE_CHOICES,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        abstract = True



class Category(models.Model):
    name            = models.CharField(max_length=50)
    description     = models.CharField(max_length=200)
    status          = models.BooleanField(default=1)

    def __str__(self):
        return str(self.name)



class Condition(models.Model):
    name            = models.CharField(max_length=50)
    description     = models.CharField(max_length=200)
    status          = models.BooleanField(default=1)

    def __str__(self):
        return str(self.name)



# class Images(models.Model):
#     # product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
#     display_image = models.ImageField(upload_to='product/', verbose_name='Image')
#     dec_image1 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image1')
#     dec_image2 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image2')
#     dec_image3 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image3')
#     dec_image4 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image4')
#     dec_image5 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image5')

#     def __str__(self):
#         return str(self.product)


class Product(models.Model):
    New = 'N'
    Old = 'O'
    CONDITION_CHOICES = (
        (New, 'New'),
        (Old, 'Old'),
    )

    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    # images              = models.ForeignKey(Images, on_delete=models.CASCADE, default=1)
    # condition           = models.CharField(max_length=1, choices=CONDITION_CHOICES, default=New)
    condition           = models.ForeignKey(Condition, on_delete=models.CASCADE)
    title               = models.CharField(max_length=100)
    published_date      = models.DateTimeField(auto_now=True)
    description         = models.CharField(max_length=5000)
    author              = models.CharField(max_length=500)
    price               = models.IntegerField()
    discount_price      = models.IntegerField(blank=True, null=True)
    total_quantity      = models.PositiveIntegerField(default=1)
    remaining_quantity  = models.PositiveIntegerField()
    pickup_address      = models.CharField(max_length=500, blank=False)
    google_maps_coordinates            = models.CharField(max_length=100)
    visit_count         = models.IntegerField(default=0)
    slug                = models.SlugField(unique=True, max_length=500)
    display_image = models.ImageField(upload_to='product/', verbose_name='Image')
    dec_image1 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image1')
    dec_image2 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image2')
    dec_image3 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image3')
    dec_image4 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image4')
    dec_image5 = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='Image5')

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        self.slug   = self._get_unique_slug()
        if not self.id:
            try:
                self.display_image  = self.compressImage(self.display_image)
            except:
                pass
            try:
                self.dec_image1     = self.compressImage(self.dec_image1)
            except:
                pass
            try:
                self.dec_image2     = self.compressImage(self.dec_image2)
            except:
                pass
            try:
                self.dec_image3     = self.compressImage(self.dec_image3)
            except:
                pass
            try:
                self.dec_image4     = self.compressImage(self.dec_image4)
            except:
                pass
            try:
                self.dec_image5     = self.compressImage(self.dec_image5)
            except:
                pass
        super(Product, self).save(*args, **kwargs)

    def compressImage(self,uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
            
    def get_add_to_cart_url(self):
         return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })




def get_image_filename(instance, filename):
    id = instance.product.id
    return "product_images/%s" % (id)



    


class Review(models.Model):
    RATING_CHOICES = (
        (1, 'one'), 
        (2, 'two'), 
        (3, 'three'), 
        (4, 'four'), 
        (5, 'five')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class ReportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title




class ProductReview(Review):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='comment/', blank=True, null=True, verbose_name='Image')
    created_date = models.DateTimeField(auto_now=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text



class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    # apartment_address = models.CharField(max_length=100)
    # country = CountryField(multiple=False)
    google_maps_coordinates = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'




class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"



class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
