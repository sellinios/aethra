from django.db import models
from django.apps import apps  # Use apps.get_model for dynamic model resolution
from django.utils import timezone

# Supplier model for managing vendors that provide products
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Inventory model to track product stock and supplier information
class Inventory(models.Model):
    product = models.OneToOneField('eshop.Product', related_name='inventory', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='supplied_products', on_delete=models.SET_NULL, null=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)  # When stock falls below this level, reorder
    last_restocked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - Stock: {self.quantity_in_stock}"

    # Method to restock inventory
    def restock(self, quantity):
        self.quantity_in_stock += quantity
        self.last_restocked_at = timezone.now()
        self.save()

# Financial record to track income, expenses, and profits for orders
class FinancialRecord(models.Model):
    order = models.OneToOneField('eshop.Order', related_name='financial_record', on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount earned from the order
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Cost of goods sold
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically calculate net profit before saving
        self.net_profit = self.income - self.expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Financial Record for Order {self.order.id}"

# Purchase Order model for ordering stock from suppliers
class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='purchase_orders', on_delete=models.CASCADE)
    product = models.ForeignKey('eshop.Product', related_name='purchase_orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField()
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"Purchase Order {self.id} - {self.product.name} from {self.supplier.name}"

    # Method to mark the order as received and update inventory
    def mark_as_received(self):
        if not self.received:
            inventory = self.product.inventory
            inventory.restock(self.quantity)
            self.received = True
            self.save()
