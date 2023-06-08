
from tabnanny import verbose
from django.db import models
from vendors.models import Vendor
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)#models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True,blank=True)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email, name=instance.user_name)
        print(instance, 'customer created')


@receiver(post_save, sender=User)
def save_customer(sender, instance, *args, **kwargs):
    instance.customer.save()


class Categories(models.Model):
    Categories = (
        ("Apparel", "Apparel"),
        ("Footware", "Footware"),
        ("Bags", "Bags"),
        ("Accessories", "Accessories"),
        ("Eyewear", "Eyewear"),
        ("Cosmetics and Beauty", "Cosmetics and Beauty"),
        ("Consumer Electronics", "Consumer Electronics"),
        ("Sporting goods", "Sporting goods"),
    )
    name = models.CharField(max_length=200, null=True, choices=Categories)
    image = models.ImageField(null=True, blank=True, upload_to="categories")
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class BrandCategories(models.Model):
    brands = (
        ("Nike", "Nike"),
        ("Adidas", "Adidas"),
        ("Balenciaga", "Balenciaga"),
        ("Dior", "Dior"),
        ("Prada", "Prada"),
        ("Vans", "Vans"),
        ("Bata", "Bata"),
        
    )
    main_categories = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, choices=brands)
    image = models.ImageField(null=True, blank=True, upload_to="brands")
    
    def __str__(self):
        return f"{self.name} {self.main_categories}"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class BrandMiniCategories(models.Model):
    brand_categories = models.ForeignKey(BrandCategories, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name}, {self.brand_categories}"
    
    # def save(self, *args, **kwargs):
    #     if not self.name:
    #         self.name = str(self.brand_categories).split(' ')[0]
    #         print(self.name)
    #     return super().save(*args, **kwargs)

class Products(models.Model):
    name = models.CharField(max_length=200)
    mainCategory = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(BrandCategories, null=True, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    price = models.FloatField()#models.DecimalField(max_digits=6, decimal_places=2)
    Brand = models.CharField(null=True,max_length=200)
    description = models.TextField(max_length=200, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="img")
    image2 = models.ImageField(null=True, blank=True, upload_to="img")
    image3 = models.ImageField(null=True, blank=True, upload_to="img")
    image4 = models.ImageField(null=True, blank=True, upload_to="img")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    
    @property
    def imageURL3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL4(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)#models.CharField(max_length=200, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    pending = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    def cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total
        
    
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
class OrderItem(models.Model):   
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    productId = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.order)
        


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)#models.CharField(max_length=200, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True) 
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    mpesacode = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.address
    
    
    
    
    
    
    
    