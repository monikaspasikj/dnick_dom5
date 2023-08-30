from django.contrib import admin

from dom.models import Product, Customer,  Order, OrderProduct

class ProductAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

class CustomerAdmin(admin.ModelAdmin):

    def has_view_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False



class OrderProductAdmin(admin.TabularInline):
    model=OrderProduct
    extra = 0

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductAdmin]



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product,ProductAdmin)
