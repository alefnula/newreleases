import click
import html2text
from newreleases.commands.cli import release
from newreleases.html import is_html
from newreleases.enums import Provider
from newreleases.utils import handle_client_errors, print_as_table


@release.command("list")
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
def release_list(config, provider, project):
    """List project releases."""
    for page in config.client.release_list(provider=provider, project=project):
        print_as_table(page)
        click.echo(
            "\nPress RETURN for the next page, any other key to stop.\n"
        )
        char = click.getchar()
        if char != "\r":
            break


@release.command("get")
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
def release_get(config, provider, project, version):
    """Get a specific release."""
    print_as_table(
        [
            config.client.release_get(
                provider=provider, project=project, version=version
            )
        ]
    )


@release.command("note")
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
def release_note(config, provider, project, version):
    """Get a release note for specific release."""
    note = config.client.release_note(
        provider=provider, project=project, version=version
    )
    click.echo()
    if note.title.strip() != "":
        click.echo(note.title)
        click.echo("=" * len(note.title))
        click.echo()
        click.echo(note.url)
    else:
        click.echo(note.url)
        click.echo("=" * len(note.url))
    click.echo()
    if is_html(note.message):
        click.echo(html2text.html2text(note.message))
    else:
        click.echo(note.message)
