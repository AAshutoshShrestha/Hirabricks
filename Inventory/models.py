import os
from dotenv import load_dotenv
from django.utils.text import slugify
from django.db import models
from django.utils.html import format_html
from supabase import create_client, Client, ClientOptions

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key,
  options=ClientOptions(
    postgrest_client_timeout=10,
    storage_client_timeout=10
  ))

class BrickCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        # If the slug is not set or the name has changed, generate the slug
        if not self.slug or self.name != self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])


class BrickProduct(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255)

    category = models.ForeignKey(BrickCategory, on_delete=models.CASCADE)
    description = models.TextField()
    dimensions = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to ='Products')
    product_code = models.CharField(max_length=10, unique=True, editable=False)

    def product_img_display(self):
        res = supabase.storage.from_('image-bucket/Products').get_public_url(self.product_image)
        return format_html('<img src="{}" width="100" height="100">', res)
    
    def save(self, *args, **kwargs):
        # If the slug is not set or the name has changed, generate the slug
        if not self.slug or self.name != self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        if not self.pk:  # Only for new instances
            last_product = BrickProduct.objects.order_by('-id').first()
            if last_product:
                last_code = last_product.product_code
                last_num = int(last_code.split('-')[1])
                new_num = last_num + 1
                self.product_code = f'HB-{str(new_num).zfill(4)}'
            else:
                self.product_code = 'HB-0001'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])
  

class Sale(models.Model):
    product = models.ForeignKey(BrickProduct, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    date_sold = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.stock -= self.quantity_sold
        self.product.save()

    def __str__(self):
        return f"{self.quantity_sold} units of {self.product.name} sold on {self.date_sold}"
    
    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])


class BrickStock(models.Model):
    product = models.ForeignKey(BrickProduct, on_delete=models.CASCADE)
    quantity_added = models.PositiveIntegerField()
    stock_in_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.stock += self.quantity_added
        self.product.save()

    def __str__(self):
        return f"{self.quantity_added} units of {self.product.name} added on {self.stock_in_date}"
    
    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])
