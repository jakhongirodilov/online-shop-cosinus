import datetime
from django.db import models
from accounts.models import Address, CustomUser



class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=70)
    description = models.CharField(max_length = 200)
    cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    paid = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name[:50]
    

class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "user_cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.product}, {self.quantity}| {self.user}"
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    cost = models.DecimalField(max_digits = 12, decimal_places = 2)
    quantity = models.IntegerField()

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=10)

    ordered_date = models.DateTimeField(default=datetime.datetime.today)
    delivery_date = models.DateTimeField(null = True, blank=True)
    is_active = models.BooleanField(default=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} - {self.customer.username}"
    
    # foydalanuvchi buyurtmani qabul qilgandan so'ng, maxsus tugmani bosish orqali buyurtma yakunlanganini bildirishi mumkin 
    def complete_order(self):
        self.is_delivered = True
        self.is_active = False
        self.save()

    # modellarning built-in save() funksiyasini override qilish orqali, yetkazib berish vaqti avtomatik aniqlanadi
    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.ordered_date + datetime.timedelta(weeks=1)

        super().save(*args, **kwargs)