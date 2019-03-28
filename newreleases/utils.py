import click
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

        return wrapper

    return decorator
