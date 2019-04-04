__all__ = [
    # Groups
    "cli",
    "project",
    "release",
    # Utils
    "shell",
    # Configuration
    "configure",
    "get_auth_key",
    # Project
    "project_list",
    "project_get",
    "project_add",
    "project_update",
    "project_delete",
    # Release
    "release_list",
    "release_get",
    "release_note",
]


from newreleases.commands.cli import cli, project, release
from newreleases.commands.utils import shell
from newreleases.commands.configuration import configure, get_auth_key
from newreleases.commands.project import (
    project_list,
    project_get,
    project_add,
    project_update,
    project_delete,
)
from newreleases.commands.release import (
    release_list,
    release_get,
    release_note,
)
