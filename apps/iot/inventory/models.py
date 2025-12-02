from django.db import models


class StorageUnit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO; How to light up the specific storage unit, ie all the compartments ?
    # 1. do we define the entire led selection here ?
    # 2. Or should we get the first compartments led start value, and the last compartments led end value ?
    # led_address_start = models.IntegerField(default=0)
    # led_address_end = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    # TODO; Should i define the storage fixed IP here or ? .. TODO TODO TODO
    # @property
    # def base_url(self):
    #     return f"http://{self.device_ip}"


class Compartment(models.Model):
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, related_name='compartments')  # nopep8
    name = models.CharField(max_length=50)
    led_address_start = models.IntegerField(default=0)
    led_address_end = models.IntegerField(default=0)
    led_count = models.IntegerField(default=8)
    max_quantity = models.PositiveIntegerField(default=10)
    low_quantity_threshold = models.PositiveBigIntegerField(blank=True,  null=True)  # nopep8
    current_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.storage_unit.name} - {self.name}"

    @property
    def low_quantity(self):
        # use the custom threshold if set, otherwise default to 20% of max_quantity.
        threshold = self.low_quantity_threshold if self.low_quantity_threshold is not None else (0.2 * self.max_quantity)  # nopep8
        return self.current_quantity < threshold

    @property
    def current_quantity(self):
        return self.inventory_set.aggregate(total=models.Sum('quantity'))['total'] or 0


class Part(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, blank=True)  # nopep8  # optional unique identifier
    manufacturer = models.CharField(max_length=100, blank=True)  # nopep8 # who made the part
    part_number = models.CharField(max_length=50, blank=True)  # nopep8 # manufacturer part number
    category = models.CharField(max_length=50, blank=True)  # nopep8 # ie resistor, capacitor, LED
    value = models.CharField(max_length=50, blank=True)  # nopep8 # ie 10kΩ, 220uF, 5V
    tolerance = models.CharField(max_length=20, blank=True)  # nopep8 # ie 1%, 5%
    voltage_rating = models.CharField(max_length=20, blank=True)  # nopep8  # ie 50V, 5V
    package_type = models.CharField(max_length=50, blank=True)  # nopep8 # ie SMD-0805, DIP-8
    quantity = models.PositiveIntegerField(default=0)  # nopep8 # total in all compartments
    compartments = models.ManyToManyField("Compartment", through='Inventory', related_name='parts')  # nopep8

    # TODO; What else could i add?

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})" if self.sku else self.name


class Inventory(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('part', 'compartment')

    def __str__(self):
        return f"{self.part.name} in {self.compartment.name} ({self.quantity})"


class LEDConfiguration(models.Model):
    compartment = models.OneToOneField(Compartment, on_delete=models.CASCADE, related_name='led_config')  # nopep8
    normal_color = models.CharField(max_length=7, default="RGB(255, 255, 255)")  # TODO; not sure about the colour codes yet # nopep8
    low_quantity_color = models.CharField(max_length=7, default="RGB(255, 255, 255)")  # TODO; not sure about the colour codes yet # nopep8
    selected_color = models.CharField(max_length=7, default="RGB(255, 255, 255)")  # TODO; not sure about the colour codes yet # nopep8
    pulse = models.BooleanField(default=False)
    blink = models.BooleanField(default=False)

    # TODO; What else to add here?

    def __str__(self):
        return f"LED config for {self.compartment.name}"
