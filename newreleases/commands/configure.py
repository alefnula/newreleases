import click
from newreleases.commands.cli import cli
from newreleases.utils import handle_client_errors


@cli.command()
@click.pass_obj
@handle_client_errors()
def configure(config):
    """Configure newreleases."""
    config.configure()
    config.save()
