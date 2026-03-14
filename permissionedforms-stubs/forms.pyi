from typing import Any

from django import forms
from django.contrib.auth.base_user import AbstractBaseUser

class Options:
    def __init__(self, options: type | None = None) -> None: ...

class OptionCollectingMetaclass(type):
    options_class: type[Options] | None
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> Any: ...

class PermissionedFormOptionsMixin:
    field_permissions: dict[str, str] | None
    def __init__(self, options: type | None = None) -> None: ...

class PermissionedFormOptions(PermissionedFormOptionsMixin, Options): ...

FormMetaclass: type[forms.forms.DeclarativeFieldsMetaclass]

class PermissionedFormMetaclass(OptionCollectingMetaclass, forms.forms.DeclarativeFieldsMetaclass):  # type: ignore[misc]
    options_class: type[PermissionedFormOptions]

class PermissionedForm(forms.Form, metaclass=PermissionedFormMetaclass):
    def __init__(self, *args: Any, for_user: AbstractBaseUser | None = None, **kwargs: Any) -> None: ...

class PermissionedModelFormOptions(PermissionedFormOptionsMixin, forms.models.ModelFormOptions): ...

class PermissionedModelFormMetaclass(PermissionedFormMetaclass, forms.models.ModelFormMetaclass):  # type: ignore[misc]
    options_class: type[PermissionedModelFormOptions]

class PermissionedModelForm(PermissionedForm, forms.ModelForm, metaclass=PermissionedModelFormMetaclass): ...  # type: ignore[misc]
