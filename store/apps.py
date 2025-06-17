from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration class for the "store" application.

    This class represents the configuration settings for the
    Django "store" application. It includes metadata such as the default
    primary key field
    type for models and the application name.

    :ivar default_auto_field: Specifies the default field type for
        auto-generated primary keys in models.
    :type default_auto_field: str
    :ivar name: The name of the application.
    :type name: str
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
