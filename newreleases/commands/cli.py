import os
import click
from newreleases import consts
from newreleases.config import Config


@click.group()
@click.option(
    "--config",
    type=click.Path(exists=True),
    envvar="NMC_CONFIG",
    help="Path to the alternative configuration file.",
)
@click.option(
    "--profile",
    default="default",
    envvar="NMC_PROFILE",
    help="Configuration file profile.",
)
@click.pass_context
def cli(ctx, config, profile):
    if config is None:
        config = os.path.expanduser(consts.DEFAULT_CONFIG_PATH)
        if (
            not os.path.isfile(config)
            and ctx.invoked_subcommand != "configure"
        ):
            click.echo("newreleases is not configured.")
            click.echo("Before usage run: newreleases configure")
            ctx.exit()
    ctx.obj = Config(config, profile)


@cli.group()
def project():
    """Project operations."""
    pass


@cli.group()
def release():
    """Project release operations."""
    pass
