from pydantic import ValidationError


def validate_input_data(model, data: dict):
    try:
        result = model(**data)
    except ValidationError as e:
        return None, e.errors()
    else:
        return result, None
