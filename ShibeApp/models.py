from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe



STATUS_CHOICE = (
   ('add', 'Added'),
   ('remove', 'Removed'),
   ('delete', 'Deleted'),
)


def user_directory_path(instance,filename):
   return 'user_{(0)/(1)}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    name = models.CharField(default= "sara (Default)", max_length=200, null=True)
    title = models.CharField(default="this is the default,title change it in profile",max_length=200,null=True)
    desc_text = "hey, there is a default text description about you that you can change"
    desc = models.CharField(default=desc_text,max_length=200,null=True)
    profile_img = models.ImageField(default="images/default.jpg",upload_to="images", null=True,blank=True)

def __str__(self):
 return self.name


class Category(models.Model):
   cid = ShortUUIDField(unique=True,length=33,max_length=33,prefix='cat',alphabet='abcdefgh12345')
   title = models.CharField(max_length=200, default='category')
   image = models.ImageField(upload_to='category',default='category.jpg')

   class Meta:
      verbose_name_plural = 'Categories'

   def category_image(self):
      return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
   
   def __str__(self):
      return self.title
   
class seller(models.Model):
   sid = ShortUUIDField(unique=True,length=33,max_length=33,prefix='cat',alphabet='abcdefgh12345')

   title = models.CharField(max_length=200, default='shibesellers')
   image = models.ImageField( upload_to='user_directory_path',default='seller.jpg')
   description = models.TextField(null=True, blank=True, default='this is the seller')

   entry_time = models.CharField(max_length=100, default='100')
   contact = models.CharField(max_length=100, default = '+255 745 989 250')
   user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)


   class Meta:
      verbose_name_plural = 'Sellers'

   def seller_image(self):
      return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
   
   def __str__(self):
      return self.title


class Product(models.Model):
      pid = ShortUUIDField(unique=True,length=30,max_length=30,prefix='cat',alphabet='abcdefgh12345')
   
      user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
      category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

      title = models.CharField(max_length=200)
      image = models.ImageField(upload_to='user_directory_path',default='product.jpg')
      description = models.TextField(null=True, blank=True, default='this is the product')

      price = models.DecimalField(max_digits=999999999,decimal_places=2, default='1.99')
      old_price = models.DecimalField(max_digits=999999999,decimal_places=2, default='2.99')

      sku = ShortUUIDField(unique=True,length=4,max_length=30,prefix='sku',alphabet='1234567890')

      date = models.DateTimeField(auto_now_add=True)
      update = models.DateTimeField(null=True,blank=True)


      class Meta:
       verbose_name_plural = 'Products'

      def product_image(self):
       return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
   
      def __str__(self):
        return self.title
      

      def get_percentage(self):
         new_price = (self.price/self.old_price)*100
         return new_price

class ProductImage(models.Model):
   images = models.ImageField(upload_to="product-images",default="product.jpg")

   product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)

   date = models.DateTimeField(auto_now_add=True)



   class Meta:
    verbose_name_plural = 'Product_images'

class Debtor(models.Model):
  
   debtor_name = models.CharField(max_length=255)
   debtor_phone = models.CharField(max_length=20)
   product_price = models.DecimalField(max_digits=10, decimal_places=2)
   name_of_products = models.CharField(max_length=255)
   products_in_debt = models.CharField(max_length=255)
   debt_pending = models.DecimalField(max_digits=10, decimal_places=2)
   debt_paid = models.DecimalField(max_digits=10, decimal_places=2)
   
   
   def __str__(self):
        return self.debtor_name

   


   

