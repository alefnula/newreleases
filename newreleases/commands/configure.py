import click
from newreleases.commands.cli import cli
from newreleases.utils import handle_client_errors, print_as_table


@cli.command()
@click.pass_obj
@handle_client_errors()
def configure(config):
    """Configure newreleases."""
    auth_key = click.prompt("Auth Key")
    config.configure(auth_key=auth_key)


@cli.command("get-auth-key")
@click.pass_obj
@handle_client_errors()
def get_auth_key(config):
    """Download auth key and save it in configuration."""
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)
    auth_keys = config.client.auth_key_list(username, password)
    if len(auth_keys) == 0:
        click.secho("No auth keys found.")
        click.secho("Go to https://newreleases.io and create an auth key.")
    else:
        print_as_table(auth_keys, show_row_number=True)
        n_auth_keys = len(auth_keys)
        selection = "0"
        while not (selection.isdigit() and 0 < int(selection) <= n_auth_keys):
            selection = click.prompt(
                "Select auth key (enter row number)"
            ).strip()

        auth_key = auth_keys[int(selection) - 1]
        config.configure(auth_key=auth_key.secret)
