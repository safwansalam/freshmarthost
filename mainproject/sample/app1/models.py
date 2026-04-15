from django.db import models

class user_register(models.Model):

    ROLE_CHOICES = [
        ('user', 'Customer'),
        ('delivery', 'Delivery Boy'),
    ]

    username = models.TextField()
    email = models.EmailField()
    mobile = models.IntegerField()
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField()
    category = models.ForeignKey('category', on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
    def __str__(self):
        return self.name

class subscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('daily','Daily'),
        ('weekly','Weekly'),
        ('monthly','Monthly'),
        ]
    plan_name=models.CharField(max_length=50)
    plan_type=models.CharField(max_length=10,choices=PLAN_CHOICES)


    # description=models.TextField()
    def __str__(self):
        return self.plan_name

class category(models.Model):
    name=models.CharField(max_length=30)



class cart(models.Model):
    user_details=models.ForeignKey(user_register,on_delete=models.CASCADE)
    product_details=models.ForeignKey(product,on_delete=models.CASCADE)
    plan_details=models.ForeignKey(subscriptionPlan,on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField()


class Wishlist(models.Model):
    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    DELIVERY_STATUS_CHOICES = [  # ✅ Separate delivery status choices
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(subscriptionPlan, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    start_date = models.DateField()          # ✅ removed auto_now=True so we can set it manually
    end_date = models.DateField()
    next_delivery = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    delivery_status = models.CharField(     # ✅ Separate delivery status field
        max_length=20,
        choices=DELIVERY_STATUS_CHOICES,
        default='pending'
    )

    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=50, blank=True, null=True)

    assigned_delivery = models.ForeignKey(
        user_register,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='delivery_orders'
    )

    delivered_on = models.DateField(null=True, blank=True)
    last_delivered = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.status}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name