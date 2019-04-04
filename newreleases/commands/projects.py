import click
from newreleases.commands.cli import cli
from newreleases.utils import handle_client_errors, print_as_table
from newreleases.enums import Provider, EmailNotification


@cli.command("project-list")
@click.option("-n", "--name", type=str, help="Filter projects by name.")
@click.pass_obj
@handle_client_errors()
def project_list(config, name=None):
    """List all projects."""
    for page in config.client.project_list(q=name or ""):
        print_as_table(page)
        click.echo(
            "\nPress RETURN for the next page, any other key to stop.\n"
        )
        char = click.getchar()
        if char != "\r":
            break


@cli.command("project-get")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.pass_obj
@handle_client_errors(m404="Project not found.")
def project_get(config, provider, project):
    """Get project by project provider and project name."""
    print_as_table(
        [config.client.project_get(provider=provider, project=project)]
    )


@cli.command("project-add")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.option(
    "--email-notifications",
    type=click.Choice(EmailNotification.choices),
    callback=EmailNotification.click_callback,
    default=EmailNotification.none,
    help="Frequency of email notifications. (Default: none)",
)
@click.pass_obj
@handle_client_errors()
def project_add(config, provider, project, email_notifications):
    """Add project."""
    print_as_table(
        [
            config.client.project_add(
                provider=provider,
                project=project,
                email_notifications=email_notifications,
            )
        ]
    )


@cli.command("project-update")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.option(
    "--email-notifications",
    type=click.Choice(EmailNotification.choices),
    callback=EmailNotification.click_callback,
    default=EmailNotification.none,
    help="Frequency of email notifications. (Default: none)",
)
@click.pass_obj
@handle_client_errors(m404="Project not found.")
def project_update(config, provider, project, email_notifications):
    """Update project."""
    print_as_table(
        [
            config.client.project_update(
                provider=provider,
                project=project,
                email_notifications=email_notifications,
            )
        ]
    )


@cli.command("project-delete")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.pass_obj
@handle_client_errors(m404="Project not found.")
def project_delete(config, provider, project):
    """Delete project."""
    if config.client.project_delete(provider=provider, project=project):
        click.echo(f"Project {provider}/{project} successfully deleted.")
    else:
        click.secho(f"Failed to delete {provider}/{project}", fg="red")


@cli.command("releases")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.pass_obj
@handle_client_errors()
def project_releases(config, provider, project):
    """List project releases."""
    for page in config.client.project_releases(
        provider=provider, project=project
    ):
        print_as_table(page)
        click.echo(
            "\nPress RETURN for the next page, any other key to stop.\n"
        )
        char = click.getchar()
        if char != "\r":
            break


@cli.command("release")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.argument("version", type=str, required=True)
@click.pass_obj
@handle_client_errors(m404="Release not found.")
def project_release(config, provider, project, version):
    """Get a specific release."""
    print_as_table(
        [
            config.client.project_release(
                provider=provider, project=project, version=version
            )
        ]
    )


@cli.command("release-note")
@click.argument(
    "provider",
    required=True,
    metavar="PROVIDER",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
)
@click.argument("project", type=str, required=True)
@click.argument("version", type=str, required=True)
@click.pass_obj
@handle_client_errors(m404="Release note not found.")
def project_release_note(config, provider, project, version):
    """Get a release note for specific release."""
    print_as_table(
        [
            config.client.project_release_note(
                provider=provider, project=project, version=version
            )
        ]
    )
