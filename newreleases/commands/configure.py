import click
from newreleases.commands.cli import cli
from newreleases.utils import handle_client_errors, print_as_table


@cli.command()
@click.pass_obj
@handle_client_errors()
def configure(config):
    """Configure newreleases."""
    api_key = click.prompt("API Key")
    config.configure(api_key=api_key)


@cli.command("get-auth-token")
@click.pass_obj
@handle_client_errors()
def get_auth_token(config):
    """Download auth token and save it in configuration."""
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)
    api_keys = config.client.tokens_list(username, password)
    if len(api_keys) == 0:
        click.secho("No api keys found.")
        click.secho("Go to https://newreleases.io and create an API key.")
    else:
        print_as_table(api_keys, show_row_number=True)
        n_api_keys = len(api_keys)
        selection = "0"
        while not (selection.isdigit() and 0 < int(selection) <= n_api_keys):
            selection = click.prompt(
                "Select api key (enter row number)"
            ).strip()

        api_key = api_keys[int(selection) - 1]
        config.configure(api_key=api_key.secret)
