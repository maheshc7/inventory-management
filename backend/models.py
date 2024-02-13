from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # image_url = models.URLField()


class Item(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    in_stock = models.PositiveIntegerField(default=0)
    available_stock = models.PositiveIntegerField(default=0)

    # Details
    units = models.CharField(max_length=50)
    min_stock = models.PositiveIntegerField(default=0)
    desired_stock = models.PositiveIntegerField(default=0)
    can_assemble = models.BooleanField(default=False)
    is_component = models.BooleanField(default=False)
    is_purchasable = models.BooleanField(default=False)
    is_salable = models.BooleanField(default=False)
    is_bundle = models.BooleanField(default=False)

    # Stocks
    total_allocated = models.PositiveIntegerField(default=0)
    allocated_to_builds = models.PositiveIntegerField(default=0)
    allocated_to_sales = models.PositiveIntegerField(default=0)
    incoming_stock = models.PositiveIntegerField(default=0)
    net_stock = models.PositiveIntegerField(default=0)
    can_build = models.PositiveIntegerField(default=0)

    # Price
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Calculate derived values before saving
        self.total_allocated = self.allocated_to_builds + self.allocated_to_sales
        # TODO: Calculate avail stock or in stock?
        self.available_stock = self.in_stock - self.total_allocated
        # self.in_stock = self.total_allocated + self.available_stock
        self.net_stock = self.available_stock + self.incoming_stock
        self.desired_stock = max(
            self.desired_stock, self.min_stock)  # TODO: Check

        super().save(*args, **kwargs)
