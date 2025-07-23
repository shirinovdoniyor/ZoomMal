from django.db import models
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, URLField, ImageField, SlugField, \
    DecimalField, PositiveIntegerField, SET_NULL, ManyToManyField, DateField, SmallIntegerField, FloatField, EmailField, \
    OneToOneField, IntegerField, BooleanField,FileField
from django.db.models.enums import IntegerChoices, TextChoices


from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

class CustomUserManager(UserManager):

    def _create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone_number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self.   _db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = EmailField(unique=True, null=True)
    phone_number = CharField(max_length=20, unique=True)
    name = CharField(max_length=255)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class ProductTag(Model):
    product_tag = CharField(max_length=255)
    tag = ForeignKey('apps.Product', on_delete=CASCADE , related_name="product_tags")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_tag


class Attribute(Model):
    name = CharField(max_length=255)

class Option(Model):
    name = CharField(max_length=255)
    attribute = ForeignKey('apps.Attribute', CASCADE, related_name='options')

class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

class SiteSettings(Model):
    description = TextField()
    phone_number = CharField(max_length=15)
    app_store = URLField(max_length=255)
    google_play = URLField(max_length=255)
    apple_gallery = URLField(max_length=255)
    youtube = URLField(max_length=255)
    favicon = URLField(max_length=255)
    telegram = URLField(max_length=255)
    tiktok = URLField(max_length=255)


class Category(MPTTModel):
    name=CharField(max_length=255)
    featured=BooleanField(default=False)
    slug=SlugField(max_length=255)
    image=ImageField(upload_to='category/')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


class CommentImages(Model):
    image=ImageField(upload_to='comment_images/')
    comment=CharField(max_length=255)

class Comment(Model):
    message=CharField(max_length=255)
    user=ForeignKey('apps.User',on_delete=CASCADE,related_name='comments')
    product=ForeignKey('apps.Product',on_delete=CASCADE,related_name='comments')


class Order(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='orders')
    status = CharField(max_length=20, default='yangi')
    total = DecimalField(max_digits=10, decimal_places=2)
    payment = ForeignKey("apps.Payment" , SET_NULL , null=True , blank=True ,related_name='orders')


class Review(Model):

    class NumberChoice(IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    number = PositiveIntegerField(choices=NumberChoice , default=NumberChoice.ONE)
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='reviews')
    product = ForeignKey("apps.Product", on_delete=CASCADE, related_name='reviews')


class UserAddress(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    phone_number_2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='user_addresses')
    email_index = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255)
    floor = models.IntegerField()
    default = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'User Addresses'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Filter(Model):
    name=CharField(max_length=255)



class FilterOption(Model):
    name=CharField(max_length=255)
    filter=ForeignKey("apps.Filter",on_delete=CASCADE,related_name='filter_options')


class ColorImage(Model):
    image = CharField(max_length=255)
    product = ForeignKey('apps.Product',CASCADE,related_name='color_images')
    name = CharField(max_length=255)
    stock = CharField(max_length=255)
    tags = ManyToManyField('apps.Tag', related_name='colorimages')

    def __str__(self):
        return self.name

class Tag(Model):
    name = CharField(max_length=255)
    def __str__(self):
        return self.name

class Badge(Model):
    name = CharField(max_length=255)
    def __str__(self):
        return self.name


class Seller(Model):
    name = CharField(max_length=255)
    country = ForeignKey('apps.Country' , CASCADE , related_name='sellers')


class Promocode(Model):
    code = CharField(max_length=255)
    discount = CharField(max_length=255)
    term = DateField()

class Advertising(Model):
    image = TextField(max_length=500)
    link = CharField(max_length=255)


class AttributeProduct(Model):
    attribute = ForeignKey('apps.Attribute', CASCADE, related_name='attribute_products')
    product = ForeignKey('apps.Product', CASCADE, related_name='attribute_products')


    def __str__(self):
        return f"{self.attribute.name} - Product {self.product}"

class Delivery(Model):
    class DeliveryType(TextChoices):
        EXPRESS = "express" , "Express"
        PICK_UP = "pick up" , "Pick Up"
        FREE = "free" , "Free"
    description = TextField()
    price = DecimalField(decimal_places=0, max_digits=10)
    deliver_type = CharField(max_length=255 , choices=DeliveryType)

class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')


class Brand(Model):
    name = CharField(max_length=255)
    icon = ImageField(upload_to='brands/')

class Country(Model):
    name = CharField(max_length=255)


class Product(Model):
    title = CharField(max_length=255)
    price = DecimalField(decimal_places=2, max_digits=10)
    discount = SmallIntegerField(default=0)
    description = TextField()
    details = TextField()
    thumbnail_image = ImageField(upload_to='products/')
    document = FileField(max_length=255,null=True,blank=True)
    seller = ForeignKey('apps.Seller', on_delete=CASCADE, related_name='products',null=True,blank=True)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')
    brand = ForeignKey('apps.Brand', on_delete=CASCADE, related_name='products',null=True,blank=True)
    badge = ForeignKey('apps.Badge', on_delete=CASCADE, related_name='products',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # Qo‘shilayotgan sana
    @property
    def discount_price(self):
        return int(self.price)-int(self.price)*(self.discount/100)
    @property
    def initial_payment(self):
        credit_amount=float(self.discount_price)+float(self.discount_price*0.22)
        return round(credit_amount*0.3,0)
    @property
    def monthly_pay(self):
        amount=(float(self.discount_price)+float(self.discount_price*0.22))-float(self.initial_payment)
        return amount/11
class PaymentPlan(Model):
    number = CharField(max_length=255)
    percentage = FloatField()

    def __str__(self):
        return self.number


class Region(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class PaymentPlanProduct(Model):
    payment_plan = ForeignKey("apps.PaymentPlan", on_delete=CASCADE , related_name="payment_plan_products")
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='payment_plan_products')

    def __str__(self):
        return f"{self.payment_plan.number} - {self.product}"


class OrderItem(Model):
    order = ForeignKey('apps.Order', on_delete=CASCADE, related_name='order_items')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='order_items')
    quantity = IntegerField(default=1)
    address  = CharField(max_length=255)

class Payment(Model):
    icon = CharField(max_length=255)
    status = CharField(max_length=255)
    type = CharField(max_length=255)
    token = CharField(max_length=255)

class OrderItemAddress(Model):
    district = CharField(max_length=255)
    longitude = FloatField()
    latitude = FloatField()
    order = ForeignKey('apps.OrderItem', on_delete=models.CASCADE, related_name='order_item_address')