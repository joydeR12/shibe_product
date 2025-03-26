from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
      PRODUCT_CHOICES = [
        ('lishe 3kg', 'Lishe 3kg'),
        ('lishe dozen', 'Lishe dozen'),
        ('Unga 25kg', 'Unga 25kg'),
        ('Unga 10kg', 'Unga 10kg'),
        ('Unga 5kg', 'Unga 5kg'),
        ('kande 25kg', 'Kande 25kg'),
    ]

      title = models.CharField(
         max_length=255,
         choices=PRODUCT_CHOICES,  # Set predefined choices
         
      )
      image = models.ImageField(upload_to='user_directory_path',default='product.jpg')
      price = models.DecimalField(max_digits=10,decimal_places=2)
      old_price = models.DecimalField(max_digits=10,decimal_places=2, default='2.99')
     
      date = models.DateTimeField(auto_now_add=True)
      update = models.DateTimeField(null=True,blank=True)


      class Meta:
         verbose_name_plural = 'Products'
         ordering = ('-date',)

      def __str__(self):
        return self.title
      

      def get_percentage(self):
         new_price = (self.price/self.old_price)*100
         return new_price

class Debtor(models.Model):
   debtor_name = models.CharField(max_length=255)
   debtor_phone = models.CharField(max_length=20)
   date_created = models.DateTimeField(auto_now_add=True)

   class Meta:
      ordering = ('-date_created',)

   
   def __str__(self):
      return self.debtor_name

   
class CartItem(models.Model):
   debitor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.IntegerField(default=1)


class DebitorOrder(models.Model):
    debitor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debt_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debt_pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        # Convert the returned value to a string
        return f'{self.debitor.debtor_name} - Total Price: {self.total_price} - Date: {self.date_created}'

    class Meta:
        ordering = ('-date_updated', '-date_created')

      


class DebitorProduct(models.Model):
      debitor_order = models.ForeignKey(DebitorOrder, on_delete=models.CASCADE)
      product = models.ForeignKey(Product, on_delete=models.CASCADE)
      quantity = models.IntegerField(default=1)
      date_created = models.DateTimeField(auto_now_add=True)
      date_updated = models.DateTimeField(auto_now=True, null=True)
      is_ordered = models.BooleanField(default=False)

      class Meta:
         ordering = ('-date_updated', '-date_created')
      
      def __str__(self):
          return self.debitor_order.debitor.debtor_name
      