from collections.abc import Iterable, MutableMapping
from typing import Any

from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList, _DataT, _FilesT

class Options:
    def __init__(self, options: type | None = None) -> None: ...

class OptionCollectingMetaclass(type):
    options_class: type[Options] | None
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> OptionCollectingMetaclass: ...

class PermissionedFormOptionsMixin:
    field_permissions: dict[str, str] | None
    def __init__(self, options: type | None = None) -> None: ...

class PermissionedFormOptions(PermissionedFormOptionsMixin, Options): ...

FormMetaclass = forms.forms.DeclarativeFieldsMetaclass

class PermissionedFormMetaclass(OptionCollectingMetaclass, forms.forms.DeclarativeFieldsMetaclass):  # type: ignore[misc]
    options_class: type[PermissionedFormOptions]

class PermissionedForm(forms.Form, metaclass=PermissionedFormMetaclass):
    def __init__(
        self,
        data: _DataT | None = None,
        files: _FilesT | None = None,
        auto_id: bool | str = "id_%s",
        prefix: str | None = None,
        initial: MutableMapping[str, Any] | None = None,
        error_class: type[ErrorList] = ...,
        label_suffix: str | None = None,
        empty_permitted: bool = False,
        field_order: Iterable[str] | None = None,
        use_required_attribute: bool | None = None,
        renderer: BaseRenderer | None = None,
        for_user: AbstractBaseUser | None = None,
    ) -> None: ...

class PermissionedModelFormOptions(PermissionedFormOptionsMixin, forms.models.ModelFormOptions): ...

class PermissionedModelFormMetaclass(PermissionedFormMetaclass, forms.models.ModelFormMetaclass):  # type: ignore[misc]
    options_class: type[PermissionedModelFormOptions]  # type: ignore[assignment]

class PermissionedModelForm(PermissionedForm, forms.ModelForm, metaclass=PermissionedModelFormMetaclass): ...  # type: ignore[misc]
