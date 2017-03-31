from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class OrderCart(models.Model):
    user = models.ForeignKey(User, null=False, related_name="company_admin")
    product = models.ForeignKey('Product')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.user.username + " " + self.product.title

def ordercart_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance.product
    product.quantity -= 1
    product.save()



post_save.connect(ordercart_post_saved_receiver, sender=OrderCart)








class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})
    def __unicode__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=120)
    product_code = models.IntegerField()
    manufacturer = models.CharField(max_length=50,blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    # active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    quantity = models.IntegerField(default=1)
    # default = models.ForeignKey(Category, related_name='default_category', null=True, blank=True)

    def __unicode__(self): #def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={'pk': self.pk})

    def get_image_url(self):
        image = self.productimage_set.first()
        if image:
            return image.image.url
        return image


def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.product.title