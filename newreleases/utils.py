import click
import tabulate
from functools import wraps
from newreleases.errors import HttpClientError


def handle_client_errors(m404=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HttpClientError as e:
                if m404 and e.status_code == 404:
                    click.secho(m404, fg="red")
                else:
                    click.secho(e.message, fg="red")
            except KeyboardInterrupt:
                click.secho("Command interrupted.", fg="red")

        return wrapper

    return decorator


def print_as_table(objects, show_row_number=False):
    """Print objects as a fancy grid table.

    Args:
        objects: List of Model instances.
        show_row_number: Should the first column be the row number.
    """
    if not isinstance(objects, list):
        objects = [objects]
    if len(objects) == 0:
        click.secho(f"No items found.", fg="red")
    else:
        headers = objects[0].__class__.headers
        if show_row_number:
            objects = [[i, *list(obj)] for i, obj in enumerate(objects, 1)]
            headers = ["#", *headers]

        click.echo(
            tabulate.tabulate(objects, headers=headers, tablefmt="fancy_grid")
        )
