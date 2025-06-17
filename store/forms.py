from django import forms
from .models import Review, Product, Store


class ReviewForm(forms.ModelForm):
    """
    Represents a form for submitting and validating reviews.

    This class is a Django ModelForm tailored for handling reviews.
    It facilitates user submission and validation of review-related data
    such as ratings and comments. By linking to a specified Django model,
    it ensures that submitted data adheres to the model's structure and
    constraints.

    :ivar Meta.model: The model associated with the form.
        This determines the data structure used for validation and storage.
    :type Meta.model: type
    :ivar Meta.fields: A list of field names that this form will expose.
        These fields are derived from the associated model.
    :type Meta.fields: list
    """
    class Meta:
        """
        Represents a Django form meta class for specifying model and fields.

        This class defines the metadata for a Django form, specifying
        the model that the form is tied to and the fields from the
        model to be used in the form. Typically used to link a form
        to a Django model while providing an explicit list of model
        fields to include in the form.

        :ivar model: The Django model to which the form is tied.
        :type model: Model
        :ivar fields: The list of fields from the model to include in the form.
        :type fields: List[str]
        """
        model = Review
        fields = ['rating', 'comment']


class ProductForm(forms.ModelForm):
    class Meta:
        """
        Class responsible for specifying metadata for the Product model,
        defining how it is serialized and which fields are included or
        excluded during serialization.

        This class is typically used in Django applications to define
        the Meta information for serializers, particularly when working
        with the Django REST framework to control the serialized output of
        the `Product` model. It explicitly removes the
        'store' field from the serialized data.

        :ivar model: The Django model associated with this Meta class.
        :type model: type
        :ivar fields: A list explicitly defining the fields to include
            during serialization.
        :type fields: list
        """
        model = Product
        fields = ['name', 'price', 'stock']


class StoreForm(forms.ModelForm):
    """
    Represents a form for handling Store model data using Django's
    ModelForm.

    This class provides a form for creating or updating instances of the
    Store model. It is linked specifically to the Store model and includes
    only the defined fields for processing. The purpose of this class is
    to simplify managing the creation and editing of Store model instances
    by utilizing Django's ModelForm functionalities.

    :ivar Meta.model: Represents the associated model (Store) for the form.
    :type Meta.model: Model
    :ivar Meta.fields: List of fields to be included in the form.
    :type Meta.fields: list
    """
    class Meta:
        model = Store
        fields = ['name']
