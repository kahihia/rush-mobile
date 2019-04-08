from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from phonenumber_field.modelfields import PhoneNumberField

from account.models import User


class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(
        upload_to='supplier/category', default='default/no_picture.png')
    is_display = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    # RESTAURANT_CATEGORY = (
    #     ('FASTFOOD', 'อาหารจานด่วน'),
    #     ('BAKERY', 'เบเกอรี่'),
    #     ('CAFE', 'คาเฟ่'),
    #     ('STEAK', 'สเต็ก'),
    #     ('CHINESE', 'อาหารจีน'),
    #     ('KOREA', 'อาหารเกาหล่ี'),
    #     ('THAI', 'อาหารไทย'),
    #     ('INDIA', 'อาหารอินเดีย'),
    #     ('ITALY', 'อาหารอิตาลี่'),
    #     ('OTHER', 'อื่นๆ'),
    # )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='supplier', null=True)
    # category = models.CharField(
    #     max_length=8,
    #     choices=RESTAURANT_CATEGORY,
    #     default='OTHER',
    #     null=True
    # )
    name = models.CharField(max_length=30)
    profile_picture = models.ImageField(
        upload_to='supplier/profile', default='default/no_picture.png')
    banner_picture = models.ImageField(
        upload_to='supplier/banner', default='default/no_picture.png')
    address = models.CharField(blank=True, max_length=150)
    description = models.CharField(blank=True, max_length=300)
    is_open = models.BooleanField('open status', default=False)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_rating(self):
        from review.models import Review
        from django.db.models import Avg
        review = Review.objects.filter(supplier=self)
        rating = review.aggregate(Avg('rate'))['rate__avg']
        if not rating:
            rating = 0
        return rating

    def get_review_count(self):
        from review.models import Review
        from django.db.models import Count
        review = Review.objects.filter(supplier=self)
        review_count = review.aggregate(Count('rate'))['rate__count']
        return review_count

    def location(self):
        return Point(self.longitude, self.latitude, srid=4326)

    def distance_from_location(self, user_location):
        return GEOSGeometry(user_location).distance(GEOSGeometry(self.location())) * 100

    @staticmethod
    def nearby(user_location):
        supplier_list = Supplier.objects.all()
        for supplier in supplier_list:
            distance = supplier.distance_from_location(user_location)
            if distance > 20:
                supplier_list = supplier_list.exclude(user=supplier.user)
        return supplier_list

    @staticmethod
    def sorted_by_distance(supplier_list, user_location):
        return sorted(supplier_list, key=lambda t: t.distance_from_location(user_location))

    @staticmethod
    def sorted_by_rating(supplier_list):
        return sorted(supplier_list, key=lambda t: t.get_rating(), reverse=True)

    @staticmethod
    def sorted_by_review_count(supplier_list):
        return sorted(supplier_list, key=lambda t: t.get_review_count(), reverse=True)


class Telephone(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    tel_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.supplier.name


class ExtraPicture(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='supplier/extra', default='default/no_picture.png')

    def __str__(self):
        return self.supplier.name


class MainCategory(models.Model):
    supplier = models.ForeignKey(
        Supplier, related_name='main_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(blank=True, max_length=150)
    is_display = models.BooleanField(default=True)

    def __str__(self):
        return self.supplier.name+' '+self.name


class SubCategory(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(blank=True, max_length=150)
    is_display = models.BooleanField(default=True)

    def __str__(self):
        return self.supplier.name+' '+self.name


class Menu(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.FloatField(null=True, blank=True, default=None)
    image = models.ImageField(
        upload_to='supplier/menu', default='supplier/menu/food_default.png')
    is_display = models.BooleanField(default=True)
    is_out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.supplier.name+' '+self.name


class SupplierQueueIndex(models.Model):
    WALKIN = 'A'
    ONLINE = 'R'
    TYPE_OF_QUEUE_CHOICES = (
        (WALKIN, 'Walk in'),
        (ONLINE, 'Online'),
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE,)
    category = models.CharField(
        choices=TYPE_OF_QUEUE_CHOICES, default=ONLINE, max_length=1)
    index = models.CharField(default='000', max_length=3)

    def __str__(self):
        return self.supplier.name

    def reset_by_day(self):
        self.index = '000'
        self.save(update_fields=['index'])
        return self.category+self.index

    def new_queue(self):
        temp = int(self.index)+1
        self.index = '{0:03}'.format(temp)
        self.save(update_fields=['index'])
        return self.category+self.index

    def get_queue_number(self):
        return self.category+self.index
