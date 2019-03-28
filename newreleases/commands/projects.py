import click
from newreleases.commands.cli import cli


@cli.command("project-list")
@click.option("-n", "--name", type=str, help="Filter projects by name.")
@click.pass_obj
def project_list(config, name=None):
    """List all projects."""
    for project in config.client.project_list(q=name or ""):
        print(project)


@cli.command("project-get")
@click.argument("project_id", type=str, required=True)
@click.pass_obj
def project_get(config, project_id=None):
    """Get project."""
    print(config.client.project_get(project_id=project_id))
