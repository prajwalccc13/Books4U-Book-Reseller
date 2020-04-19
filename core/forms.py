from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from .models import (
    Product, 
    # Images, 
    User_Customer, 
    User_Company,
    # Comment,
)

# class CustomSignupForm(SignupForm):
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )

#     first_name = forms.CharField(max_length=30, label='First Name')
#     last_name = forms.CharField(max_length=30, label='Last Name')
#     # gender = forms.ChoiceField(choices=GENDER_CHOICES)

#     def save(self, request, user):
#         user = User()
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         # user.gender = self.cleaned_data['gender']
#         user = super(CustomSignupForm, self).save(request)
#         return user

USER_TYPE_CHOICES = (
        ('CR', 'Customer'),
        ('HR', 'HR'),
        ('RM', 'Report_Manager'),
        ('DB', 'Delivery_Boy'),
        ('CQ', 'Customer_Queries_Replier'),
    )


class SignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        # role = request.session.get('user_type')
        # group = role or "Default"
        # g = Group.objects.get(name=group)
        # user.groups.add(g)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.superuser = True
        user.save()
        return user


# class SignupForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)

#     class Meta:
#         model = User_Customer
#         fields = (
#             'first_name',
#             'last_name',
#         )



class ProductForm(forms.ModelForm):
    New = 'N'
    Old = 'O'
    CONDITION_CHOICES = (
        (New, 'New'),
        (Old, 'Old'),
    )

    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=2000, label='Item Description')
    condition           = forms.CharField(max_length=1)
    author              = forms.CharField(max_length=200)
    price               = forms.IntegerField()
    total_quantity      = forms.IntegerField()

    class meta:
        model = Product
        fields = ('title', 'description', 'condition', 'author', 'price', 'total_quantity')


# class CommentForm(forms.ModelForm):
#         class Meta:
#             model = Comment
#             fields = ('author', 'text',)


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    # shipping_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    # billing_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


# class ImageForm(forms.ModelForm):
#     display_image = forms.ImageField()
#     dec_image1 = forms.ImageField()
#     dec_image2 = forms.ImageField()
#     dec_image3 = forms.ImageField()
#     dec_image4 = forms.ImageField()
#     dec_image5 = forms.ImageField()
    
#     class meta:
#         model = Images
#         fields = ('Display Image', 'Descriptive Image1', 'Descriptive Image2','Descriptive Image3', 'Descriptive Image4', 'Descriptive Image5')
