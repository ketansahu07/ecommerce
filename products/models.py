from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# Create your models here.

## CATEGORY MODEL

class Category(models.Model):
    title = models.CharField(max_length=225, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug })

## PRODUCTS MODELS AND MANAGEMENT

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def gt_related(self, instance):
        products_one = self.get_queryset().filter(categories__in=instance.categories.all())
        products_two = self.get_queryset().filter(default=instance.default)
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs

class Product(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True, on_delete=models.CASCADE)

    objects = ProductManager()  # this returns the custom selected objects as described in the ProductManager class

    class Meta:
        ordering = ['-title']    # order the list according to the title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def get_image_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url 
        return img      # None

def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split('.')
    new_filename = f'{slug}-{instance.product.id}.{file_extension}'
    return f'products/{slug}/{new_filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.title

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    # GET_HTML_PRICE IS NEEDED HERE OR NOT?

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def add_to_cart(self):
        return f'{reverse("cart")}?item={self.id}&qty=1'

    def remove_from_cart(self):
        return f'{reverse("cart")}?item={self.id}&qty=1&delete=True'

    def get_title(self):
        return f'{self.product.title} - {self.title}'

def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variation = product.variation_set.all()
    if variation.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = product.title
        new_var.price = product.price
        new_var.sale_price = product.price
        new_var.save()

post_save.connect(product_post_saved_receiver, sender=Product)