from django.db import models
from .category import Category

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    uploaded_by = models.CharField(max_length=250)
    image = models.ImageField(upload_to='uploads/products/')
    count = models.IntegerField(default=1)  # New field for tracking stock count
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids, count__gt=0)  # Hide products with zero count

    @staticmethod
    def get_all_products():
        return Products.objects.filter(count__gt=0)  # Only show products with count > 0

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id, count__gt=0)
        else:
            return Products.get_all_products()
