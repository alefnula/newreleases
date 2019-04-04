import click
from newreleases.commands.cli import project
from newreleases.utils import handle_client_errors, print_as_table
from newreleases.enums import Provider, EmailNotification


@project.command("list")
@click.option("-n", "--name", type=str, help="Filter projects by name.")
@click.option(
    "-p",
    "--provider",
    type=click.Choice(Provider.choices),
    callback=Provider.click_callback,
    help="Filter projects by provider",
)
@click.pass_obj
@handle_client_errors()
def project_list(config, name=None, provider=None):
    """List all projects."""
    for page in config.client.project_list(query=name, provider=provider):
        print_as_table(page)
        click.echo(
            "\nPress RETURN for the next page, any other key to stop.\n"
        )
        char = click.getchar()
        if char != "\r":
            break


@project.command("get")
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


@project.command("add")
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


@project.command("update")
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


@project.command("delete")
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
        click.echo(f"Project {provider.value}:{project} successfully deleted.")
    else:
        click.secho(f"Failed to delete {provider}/{project}", fg="red")
