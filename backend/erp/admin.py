from django.contrib import admin
from .models import Supplier, Inventory, FinancialRecord, PurchaseOrder

# Register the Supplier model
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'city', 'created_at')
    search_fields = ('name', 'email', 'city')
    list_filter = ('created_at', 'city')

# Register the Inventory model
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'quantity_in_stock', 'reorder_level', 'last_restocked_at')
    search_fields = ('product__name', 'supplier__name')
    list_filter = ('supplier', 'last_restocked_at')

# Register the FinancialRecord model
@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ('order', 'income', 'expenses', 'net_profit', 'created_at')
    search_fields = ('order__id',)
    list_filter = ('created_at',)

# Register the PurchaseOrder model
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'product', 'quantity', 'order_date', 'expected_delivery_date', 'received')
    search_fields = ('product__name', 'supplier__name')
    list_filter = ('order_date', 'expected_delivery_date', 'received')

    # Action to mark selected orders as received in the admin interface
    actions = ['mark_selected_as_received']

    def mark_selected_as_received(self, request, queryset):
        queryset.update(received=True)
        for po in queryset:
            po.mark_as_received()
        self.message_user(request, f"{queryset.count()} purchase orders marked as received.")

    mark_selected_as_received.short_description = "Mark selected orders as received"
