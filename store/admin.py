from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Store, Product


class UserAdmin(BaseUserAdmin):
    """
    Extension of the BaseUserAdmin class for customization of the
    user administration interface.

    This class modifies the default user administration interface
    by extending the BaseUserAdmin class. It adds new fields and
    configurations related to the user's role, enhancing the management
    capabilities for user-related data.

    :ivar fieldsets: The fieldsets configuration, augmented with
        fields for additional user information.
    :type fieldsets: Tuple

    :ivar add_fieldsets: The add_fieldsets configuration,
        extended with fields for entering additional user information
        at the time of user creation.
    :type add_fieldsets: Tuple

    :ivar list_display: Fields to be displayed in the user list view
        in the administration interface.
    :type list_display: Tuple
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'role', 'is_staff')



class ProductInline(admin.TabularInline):
    """
    Integrates a tabular inline interface for the Product model in admin.

    This class is used in Django's admin interface to facilitate the
    inline creation and management of Product objects associated
    with a parent model. The interface displays a table that allows
    easy management of related Product objects directly within the
    parent model's admin page by showing a predefined number of
    empty forms for quick entry.

    :ivar model: The Django model associated with this inline.
    :type model: type
    :ivar extra: Number of blank forms displayed in the tabular inline.
    :type extra: int
    """
    model = Product
    extra = 1  # Number of empty product forms to show


class StoreAdmin(admin.ModelAdmin):
    """
    Administration interface for managing store information.

    This class provides functionality to manage and display store details
    in the Django admin interface. It allows for configuring inlines,
    specifying displayed fields, and customizing the admin interface
    for better store management.

    :ivar inlines: List of inline models to be included in this admin view.
    :type inlines: list
    :ivar list_display: Sequence of field names to display in the list view
        of this admin interface.
    :type list_display: tuple
    """
    inlines = [ProductInline]
    list_display = ('name', 'owner', 'created_at')


# Register models with the admin
admin.site.register(User, UserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product)
