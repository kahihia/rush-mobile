from django.db import models
from django.http import HttpResponse

from customer.models import Customer
from supplier.models import Supplier, Menu, SupplierQueueIndex
# Create your models here.


class Order(models.Model):
    DEFAULT = 0
    WAITING = 1
    COOKING = 2
    DONE = 3
    CANCEL = 4
    SUCCESS = 5
    TIMEOUT = 6

    STATUS_CHOICE = (
        (DEFAULT, 'Default'),
        (WAITING, 'Waiting'),
        (COOKING, 'Cooking'),
        (DONE, 'Done'),
        (CANCEL, 'Cancel'),
        (SUCCESS, 'Success'),
        (TIMEOUT, 'Timeout'),
    )

    ONLINE = 'R'
    WALKIN = 'A'

    CATEGORY_CHOICE = (
        (WALKIN, 'Walk in'),
        (ONLINE, 'Online')
    )

    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=STATUS_CHOICE)
    total = models.FloatField(null=True, default=None)
    special_request = models.CharField(blank=True, max_length=250)
    estimate_time = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    discount = models.FloatField(default=0.0)
    category = models.CharField(
        choices=CATEGORY_CHOICE, default=ONLINE, max_length=1)

    def __str__(self):
        return str(self.id)

    def create_order(self, customer_id, supplier_id, total, special_request, discount, menus, category):
        customer = Customer.objects.get(user__id=customer_id)
        supplier = Supplier.objects.get(user__id=supplier_id)
        order = Order.objects.create(customer=customer, supplier=supplier, total=total,
                                     special_request=special_request, discount=discount, status=1, category=category)
        order.save()
        order_menu = []
        for menu in menus:
            order_menu.append(OrderMenu.create_order_menu(
                self, order, menu['menu_id'], menu['amount']))
        return order

    def get_timestamp(self):
        return self.timestamp.strftime("%H:%M %d-%B-%Y")

    def get_order_id(self):
        return '{0:08}'.format(self.id)


class OrderMenu(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return '{0:08}'.format(self.id)

    def create_order_menu(self, order, menu_id, amount):
        menu = Menu.objects.get(id=menu_id)
        order_menu = OrderMenu.objects.create(
            order=order, menu=menu, amount=amount)
        order_menu.save()
        return order_menu


class Queue(models.Model):
    DEFAULT = 0
    INPROCESS = 1
    DONE = 2
    STATUS_CHOICE = (
        (DEFAULT, 'Default'),
        (INPROCESS, 'Inprocess'),
        (DONE, 'DONE'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICE, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    queue_number = models.CharField(default='A000', max_length=8)

    def __str__(self):
        return self.order.get_order_id()+' '+self.queue_number

    def get_timestamp(self):
        return self.timestamp.strftime("%H:%M %d-%B-%Y")

    def create_queue(self, order):

        supplier_queue, create = SupplierQueueIndex.objects.get_or_create(
            supplier=order.supplier, category=order.category)
        supplier_queue.save()
        queue = Queue.objects.create(
            order=order, queue_number=supplier_queue.new_queue(), status=1)
        queue.save()
        return queue.queue_number