from base64 import b64encode
from newreleases.pages import Pages
from newreleases.http import HttpClient
from newreleases.enums import Provider, SortOrder, EmailNotification
from newreleases.schemas import (
    ProjectSchema,
    AuthKeySchema,
    ReleaseSchema,
    ReleaseNoteSchema,
)


class Client(object):
    """NewReleases client.

    Args:
        config (newreleases.config.Config): Instance of the newreleases
            configuration.
    """

    Provider = Provider

    def __init__(self, config):
        self.config = config
        self.client = HttpClient(url=config.url, auth_key=config.auth_key)

        # Schemas
        self._project_schema = ProjectSchema()
        self._auth_key_schema = AuthKeySchema()
        self._release_schema = ReleaseSchema()
        self._release_note_schema = ReleaseNoteSchema()

    def auth_key_list(self, email, password):
        """Return a list of auth keys..

        Args:
            email (str): Users email address.
            password (str): Password for the newreleases.io website.

        list of newreleases.models.AuthKey: List of authentication keys.
        """
        auth = b64encode(f"{email}:{password}".encode("utf-8")).decode("utf-8")
        headers = {"Authorization": f"Basic {auth}"}
        result = self.client.get("/auth/keys", headers=headers)
        if "keys" in result:
            return self._auth_key_schema.load(result["keys"], many=True)
        return []

    def project_list(self, q="", sort=SortOrder.name, reverse=False, page=1):
        """List all projects.

        Args:
            q: (str): Query string. Default: “”.
            sort: (SortOrder): How to sort projects. Default: SortOrder.name
            reverse (bool): Sort in reverse order.
            page (int): Starting page. Default: 1.

        Returns:
            Pages: Pages iterator.
        """
        params = {"page": page}
        if q:
            params["q"] = q
        else:
            params["sort"] = sort.value
            if reverse:
                params["reverse"] = reverse

        return Pages(self.client, url="/projects", params=params)

    def project_get(self, provider, project):
        """Get project.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.

        Returns:
            newreleases.models.Project: Requested project.
        """
        return self._project_schema.load(
            self.client.get(f"/projects/{provider.value}/{project}")
        )

    def project_add(
        self,
        provider,
        project,
        email_notifications=EmailNotification.none,
        slack_channels=None,
        hangouts_chat_webhooks=None,
        microsoft_teams_webhooks=None,
        webhooks=None,
        exclude_version_regexp=None,
        exclude_prereleases=False,
        exclude_updated=False,
    ):
        """Add project.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.
            email_notifications (EmailNotifications): How often you want to be
                notified about this project.
            slack_channels (list of str): List of slack channel names.
            hangouts_chat_webhooks (list of str): List of hangout webhooks.
            microsoft_teams_webhooks (list of str): List of MicroSoft team
                webhooks.
            webhooks (list of str): List of webhooks.
            exclude_version_regexp (list of str): Array of version exclusion
                regular expressions.
            exclude_prereleases (bool): Exclude pre-releases.
            exclude_updated (bool): Exclude updated.

        Returns:
            newreleases.models.Project: Created project.
        """
        data = {
            "provider": provider.value,
            "name": project,
            "email_notifications": email_notifications.value,
            "exclude_prereleases": exclude_prereleases,
            "exclude_updated": exclude_updated,
        }
        if slack_channels:
            data["slack_channels"] = slack_channels
        if hangouts_chat_webhooks:
            data["hangouts_chat_webhooks"] = hangouts_chat_webhooks
        if microsoft_teams_webhooks:
            data["microsoft_teams_webhooks"] = microsoft_teams_webhooks
        if webhooks:
            data["webhooks"] = webhooks
        if exclude_version_regexp:
            data["exclude_version_regexp"] = exclude_version_regexp

        return self._project_schema.load(
            self.client.post(f"/projects", data=data)
        )

    def project_update(
        self,
        provider,
        project,
        email_notifications=EmailNotification.none,
        slack_channels=None,
        hangouts_chat_webhooks=None,
        microsoft_teams_webhooks=None,
        webhooks=None,
        exclude_version_regexp=None,
        exclude_prereleases=False,
        exclude_updated=False,
    ):
        """Update project.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.
            email_notifications (EmailNotifications): How often you want to be
                notified about this project.
            slack_channels (list of str): List of slack channel names.
            hangouts_chat_webhooks (list of str): List of hangout webhooks.
            microsoft_teams_webhooks (list of str): List of MicroSoft team
                webhooks.
            webhooks (list of str): List of webhooks.
            exclude_version_regexp (list of str): Array of version exclusion
                regular expressions.
            exclude_prereleases (bool): Exclude pre-releases.
            exclude_updated (bool): Exclude updated.

        Returns:
            newreleases.models.Project: Updated project.
        """
        data = {
            "email_notifications": email_notifications.value,
            "exclude_prereleases": exclude_prereleases,
            "exclude_updated": exclude_updated,
        }
        if slack_channels:
            data["slack_channels"] = slack_channels
        if hangouts_chat_webhooks:
            data["hangouts_chat_webhooks"] = hangouts_chat_webhooks
        if microsoft_teams_webhooks:
            data["microsoft_teams_webhooks"] = microsoft_teams_webhooks
        if webhooks:
            data["webhooks"] = webhooks
        if exclude_version_regexp:
            data["exclude_version_regexp"] = exclude_version_regexp

        self.client.post(f"/projects/{provider.value}/{project}", data=data)

    def project_delete(self, provider, project):
        """Delete project.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.

        Returns:
            bool: True if the project is successfully deleted, False otherwise.
        """
        result = self.client.delete(f"/projects/{provider.value}/{project}")
        return isinstance(result, dict) and result.get("code", None) == 200

    def project_releases(self, provider, project):
        """List Project Releases.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.

        Returns:
            Pages: Pages iterator.
        """
        return Pages(
            self.client, url=f"/projects/{provider.value}/{project}/releases"
        )

    def project_release(self, provider, project, version):
        """Get a specific project release.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.
            version (str): Version of the release.

        Returns:
            newreleases.models.Release: Release object.
        """
        return self._release_schema.load(
            self.client.get(
                f"/projects/{provider.value}/{project}/releases/{version}"
            )
        )

    def project_release_note(self, provider, project, version):
        """Get release note for a specific version.

        Args:
            provider (Provider): Name of the provider.
            project (str): Name of the project.
            version (str): Version of the release.
        """
        return self._release_note_schema.load(
            self.client.get(
                f"/projects/{provider.value}/{project}/releases/{version}/note"
            )
        )
