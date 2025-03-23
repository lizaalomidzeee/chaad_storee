from django.db import models
from config.util_models.models import TimeStampModel
from products.choices import Currency
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Product(TimeStampModel):
    name = models.CharField(max_length=225)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(
        max_length=225,
        choices = Currency.choices,
        default=Currency.GEL)
    quantity = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name


class ProductTag(TimeStampModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='tags')
    
    def __str__(self):
        return self.name


class Review(TimeStampModel, models.Model):
    user = models.ForeignKey('users.User', related_name='review', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    
    def __str__(self):
        return self.content
    
    class Meta:
        unique_together = ['product', 'user']
    



class Cart(TimeStampModel):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', related_name='carts', on_delete=models.CASCADE)




class FavoriteProduct(TimeStampModel):
    product = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='favorite_products', on_delete=models.SET_NULL, null=True, blank=True)


from config.utils.image_validators import validate_image_count, validate_image_size, validate_image_resolution
class ProductImage(TimeStampModel):
    image = models.ImageField(upload_to='products/', validators=[validate_image_size, validate_image_resolution])
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)
        
    def clean(self):
        if self.product_id:
            validate_image_count(self.product_id)
        super().clean()   

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs) 
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete= models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_of_addition = models.FloatField()
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} items"
    
    def total_price(self):
        return self.quantity * self.price_at_time_of_addition
    
    
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
