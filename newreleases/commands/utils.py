import click
from newreleases.commands.cli import cli
from newreleases.models import AuthKey, Project, Release, ReleaseNote


SHELL_HEADER = "\n".join(
    [
        "\033[36mWelcome to newreleases shell.\033[0m",
        "",
        "",
        "Available variables:",
        "",
        "\033[94mconfig\033[0m (\033[95mnewreleases.config.Config\033[0m): "
        "Configured NewReleases config.",
        "\033[94mclient\033[0m (\033[95mnewreleases.client.Client\033[0m): "
        "Configured NewReleases client.",
        "",
        "",
        "Available models:",
        "",
        "\033[94mAuthKey, Project, Release, ReleaseNote\033[0m",
    ]
)


@cli.command()
@click.pass_obj
def shell(config):
    """Run IPython shell with loaded configuration, client and models."""
    try:
        from IPython import embed

        user_ns = {
            "config": config,
            "client": config.client,
            "AuthKey": AuthKey,
            "Project": Project,
            "Release": Release,
            "ReleaseNote": ReleaseNote,
        }
        embed(user_ns=user_ns, colors="neutral", header=SHELL_HEADER)
    except ImportError:
        click.secho("IPython is not installed", fg="red")
