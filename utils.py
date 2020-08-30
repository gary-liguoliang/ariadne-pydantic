from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


def to_camel_case(string: str) -> str:
    if '_' in string:
        n = string.title().replace('_', '')
    else:
        n = string
    return ''.join([n[0].lower(), n[1:]])


def translate_py_type_to_gql_type(cls) -> str:
    if cls == UUID:
        return 'ID'
    elif issubclass(cls, str):
        return 'String'
    elif cls == bool:
        return 'Boolean'
    elif issubclass(cls, int):
        return 'Int'
    elif cls == float:
        return 'Float'
    elif issubclass(cls, date):
        return 'String'
    elif issubclass(cls, Decimal):
        return 'String'
    elif issubclass(cls, BaseModel):
        return cls.__qualname__
    else:
        raise NotImplementedError(f'Unsupported type: {cls}')


def translate_filed_model_to_gql_type(field_model) -> str:
    is_list = False
    if hasattr(field_model.outer_type_, '_name'):
        if getattr(field_model.outer_type_, '_name', '') == 'List':
            field_model_type = field_model.type_
            is_list = True
        else:
            raise NotImplementedError(
                f'Unsupported collection type: {field_model.type_}',
            )
    else:
        field_model_type = field_model.type_
    gql_type = translate_py_type_to_gql_type(field_model_type)
    return f'[{gql_type}]' if is_list else gql_type
