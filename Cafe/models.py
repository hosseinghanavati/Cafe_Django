import random

from django.db import models
from django.utils import timezone

from .validator import *


# Create your models here.


class Table(models.Model):
    number = models.IntegerField(verbose_name="table number", help_text="enter number of table")
    position = models.CharField(max_length=50, verbose_name="table position", help_text="enter position of table")
    status = models.IntegerField(verbose_name="table status", help_text="status of table at the moment",
                                 default=0)

    def __str__(self):
        return f"{self.position}-{self.number}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='categories/images/', blank=True, null=True, verbose_name="category image",
                             help_text='upload the category image')

    def __str__(self):
        return f"{self.name}-{self.image}"


class MenuItem(models.Model):
    name = models.CharField(max_length=50, verbose_name='menu item name', help_text='add menu item name to this field')
    price = models.FloatField(verbose_name='price(dollar)', help_text='add price of menu item')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category',
                                 help_text='choose category')
    discount = models.FloatField(verbose_name='discount', help_text='insert the discount 0 to 100',
                                 validators=[discount_validator])
    serving_time_period = models.IntegerField(null=True, help_text='insert how much time spend to be served')
    estimated_cooking_time = models.IntegerField(null=True, help_text='insert how much time spend to be cooked')
    create_timestamp = models.DateTimeField(auto_now_add=True, null=True)
    modify_timestamp = models.DateTimeField(auto_now=True, null=True)

    def menu_item_final_price(self):
        final_price = self.price - ((self.price * self.discount) / 100)
        return final_price

    @classmethod
    def filter_by_category(cls, category):
        query = cls.objects.filter(category=category)
        return query

    @classmethod
    def max_price(cls):
        query = cls.objects.aggregate(models.Max("price"))
        return query

    @classmethod
    def avg_price(cls):
        query = cls.objects.aggregate(models.Avg("price"))
        return query

    def __str__(self):
        return f"{self.name}"


class OrderMenuItem(models.Model):
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)
    menu_item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="number of menu item that ordered",
                                   help_text="enter number of item you want")

    @classmethod
    def filter_by_menuitem(cls, menu_item):
        query = cls.objects.filter(menu_item_id=menu_item.id)
        return query

    @classmethod
    def filter_by_menuitem_category(cls, category):
        query = cls.objects.filter(menu_item_id__category=category)
        return query

    def __str__(self):
        return f"{self.order_id}-{self.menu_item_id}-{self.quantity}"


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, verbose_name="set status of this order", help_text="choose between 0,1,2")
    number = models.IntegerField(default=random.randint(100, 10000000))
    datetime_stamp = models.DateTimeField(auto_now_add=True, verbose_name="time that order recorded")
    menu_items = models.ManyToManyField(MenuItem, through=OrderMenuItem, through_fields=["order_id", "menu_item_id"])

    @classmethod
    def today_orders(cls):
        query = cls.objects.filter(datetime_stamp__day=timezone.now().day)
        return query

    @classmethod
    def month_orders(cls):
        query = cls.objects.filter(datetime_stamp__month=timezone.now().month)
        return query

    def __str__(self):
        return f"number:{self.number}-items:{self.menu_items.all()}-Date:{self.datetime_stamp}"


class Receipt(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.IntegerField(verbose_name="price of order")
    final_price = models.IntegerField(verbose_name="price of order with discounts")
    date_time_stamp = models.DateTimeField(verbose_name="publish time of receipt", default=timezone.now)

    def __str__(self):
        return f"{self.order_id}"
