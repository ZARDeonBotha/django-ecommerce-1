from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Store, Product


# Extend the default UserAdmin to include the custom 'role' field
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')


# Inline product management within each Store
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Number of empty product forms to show


# Customize Store admin to include inline product editing
class StoreAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('name', 'owner', 'created_at')


# Register models with the admin
admin.site.register(User, UserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product)
