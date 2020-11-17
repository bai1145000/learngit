from django.test import TestCase

# Create your tests here.
def get_image_path(instance, filename):
    name = instance.product.product_name
    return 'picture/%s/%s' % (name,filename)