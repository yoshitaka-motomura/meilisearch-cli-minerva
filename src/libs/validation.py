import click
from src.libs import libs


def validate_exists_index_name(ctx, param, value):
    if value is None:
        return None
    try:
        if libs.is_exists_index(value):
            raise click.BadParameter("An index that already exists.")
        return value
    except ValueError:
        raise click.BadParameter("failed")


def validate_not_exists_index_name(ctx, param, value):
    if value is None:
        return None
    try:
        if not libs.is_exists_index(value):
            raise click.BadParameter("Specified index does not exist")
        else:
            return value
    except ValueError:
        raise click.BadParameter("failed")
