from decimal import Decimal

import humps
from pydantic import AliasChoices, AliasGenerator, BaseModel as BaseRow


def serialization_field(field: str):
	return humps.camelize(field)


def alias_resolve(field: str):
	return AliasChoices(field, humps.camelize(field), humps.pascalize(field))


# by default convert model to camelCase
class BaseModel(BaseRow):
	model_config = {
		"populate_by_name": True,
		"from_attributes": True,
		"arbitrary_types_allowed": True,
		"alias_generator": AliasGenerator(alias=serialization_field, validation_alias=alias_resolve),
		"json_encoders": {
			Decimal: lambda v: str(v),
			ValueError: lambda v: str(v),
			bytes: lambda v: v.hex(),
		},
	}
