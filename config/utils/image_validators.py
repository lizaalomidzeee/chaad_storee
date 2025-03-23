from django.core.validators import ValidationError
from django.apps import apps
from PIL import Image


def validate_image_size(image):
    size = image.size
    limit = 5
    if size >= limit * 1024 * 1024:
        raise ValidationError(f"სურათის ზომა არ უნდა აღემატებოდეს {limit} MB")
    

def validate_image_resolution(image):
    min_height, min_width = 300, 300
    max_height, max_width = 4000, 4000
    img = Image.open(image)
    img_width, img_height = img.size

    if img_width >= max_width or img_height >= max_height:
        raise ValidationError("მაქსიმალური დაშვებული სურათის გაფართოება არის 4000x4000 პიქსელი")
    if img_width <= min_width or img_height <=  min_height:
        raise ValidationError("მინმალური დაშვებული სურათის გაფართოება არის 300x300 პიქსელი")
    


def validate_image_count(product_id):
    ProductImage = apps.get_model("products", "ProductImage")
    limit = 5
    count = ProductImage.objects.filter(product_id=product_id).count()
    if count >= limit:
        raise ValidationError('1 პროდუქტზე დაშვებულია მაქსიმუმ 5 სურათის ატვირთვა')