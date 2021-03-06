from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


# define product model
class Product(models.Model):

    CONDITION_TYPE = (
        ("new", "New product"),
        ("used", "Used product"),
        ("damaged", "Damaged product")
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/images/main_product_images',
                              # when we have no image, we use default image
                              default='product/images/default_images/no-image.png',
                              blank=True,
                              null=True)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    condition = models.CharField(max_length=100,
                                 choices=CONDITION_TYPE)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True)
    brand = models.ForeignKey('Brand',
                              on_delete=models.SET_NULL,
                              null=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2)
    created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True,
                            null=True)

    # create slug using name field when saving object
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            # create slug using two different fields, in this case name and created date

            self.slug = '-'.join((slugify(self.name), slugify(self.created)))
        super(Product, self).save(*args, *kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


# Images handler for product model (more than one image ?)
class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/product_images',
                              blank=True,
                              null=True)

    def __str__(self):
        
        return self.product.name


# define category model
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product/images/category_images',
                              blank=True,
                              null=True)

    slug = models.SlugField(blank=True,
                            null=True)

    # create slug using category_name field when saving object
    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, *kwargs)

    # display correctly plural form of class name
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


# define brand model
class Brand(models.Model):
    brand_name = models.CharField(max_length=50)

    def __str__(self):
        return self.brand_name
