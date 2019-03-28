import click
from newreleases.commands.cli import cli


@cli.command()
@click.pass_obj
def shell(config):
    """Run IPython shell with loaded configuration."""
    try:
        from IPython import embed

        user_ns = {"config": config}
        embed(user_ns=user_ns, colors="neutral")
    except ImportError:
        click.secho("IPython is not installed", fg="red")
