from datetime import date as dt
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class CarModel(models.Model):
    make = models.CharField(
        max_length=200,
        help_text='Enter vehicles maker'
    )
    model = models.CharField(
        max_length=200,
        help_text='Enter vehicles model'
    )
    description = models.TextField(
        max_length=2000,
        default='',
        blank=True,
    )
    photo_link = models.CharField(
        'Link to photo',
        max_length=330,
        default='',
    )

    def __str__(self):
        return f'{self.make} {self.model}'


class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.RESTRICT,
        null=True)
    description = HTMLField(default="")
    VIN_code = models.CharField(
        max_length=200
    )
    plate_number = models.CharField(
        max_length=200,
        help_text='Enter vehicles plate number'
    )
    client = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return f'{self.car_model} {self.plate_number} {self.client} {self.VIN_code}'

    def display_order(self):
        return ", ".join(str(order.id) for order in self.orders.all())

    display_order.short_description = "Order"


class OrderRow(models.Model):
    service = models.ForeignKey(
        'Service',
        on_delete=models.RESTRICT,
        null=True,
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.RESTRICT,
        null=True,
        related_name='order_rows'
    )
    date = models.DateField(
        help_text='Enter date',
    )
    price = models.FloatField(
        help_text='Enter price',
    )

    def __str__(self):
        return f'{self.service} {self.price} {self.date}'


class Service(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Enter name of the service'
    )
    price = models.FloatField(
        help_text='Enter price'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "Service"


class OrderQuerySet(models.QuerySet):

    def done(self):
        return self.filter(status__exact="f")

    def order_by_due_back(self):
        return self.order_by("due_back")


class Order(models.Model):
    objects = OrderQuerySet.as_manager()
    car_owner = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.RESTRICT,
        null=True,
        related_name='order'
    )
    service = models.ManyToManyField(
        Service,
        through=OrderRow,
    )
    description = models.TextField(
        null=True,
        blank=True,
        max_length=200,
    )
    date = models.DateField(
        'Date',
        null=True,
        blank=True,
    )
    due_back = models.DateField(
        "Will be returned",
        null=True,
        blank=True,
    )
    ORDER_STATUS = (
        ('r', 'Registered'),
        ('a', 'Vehicle awaiting for diagnostic'),
        ('br', 'Vehicle is being repaired'),
        ('f', 'Fixed, ready to be returned')
    )

    status = models.CharField(
        max_length=15,
        choices=ORDER_STATUS,
        blank=True,
        default='r',
        help_text='STATUS',
    )

    def total_order_row_price(self):
        total_amount = self.order_rows.all().aggregate(result=Sum('price'))
        return f'{total_amount["result"]}'

    total_order_row_price.short_description = 'Total'

    def display_services(self):
        service = ', '.join(service.name for service in self.service.all())
        return f'{service}'

    display_services.short_description = 'Services'

    def __str__(self):
        return f'{self.id} {self.status}'

    def save(self, *args, **kwargs):
        self.amount = self.total_order_row_price()
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.due_back and dt.today() > self.due_back:
            return True
        return False

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderReview(models.Model):
    order = models.ForeignKey("Order", on_delete=models.RESTRICT, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField("Comment", max_length=2000)
