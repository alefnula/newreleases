import enum
from newreleases.page import Pages
from newreleases.http import HttpClient
from newreleases.schemas import ProjectSchema


class SortOrder(enum.Enum):
    name = "name"
    updated = "updated"
    added = "added"


class Client(object):
    """NewReleases client.

    Args:
        config (newreleases.config.Config): Instance of the newreleases
            configuration.
    """

    def __init__(self, config):
        self.config = config
        self.client = HttpClient(url=config.url, api_key=config.api_key)

        # Schemas
        self._project_schema = ProjectSchema()

    def project_list(self, q="", sort=SortOrder.name, reverse=False, page=1):
        """List all projects.

        Args:
            q: (str): Query string. Default: “”.
            sort: (SortOrder): How to sort projects. Default: SortOrder.name
            reverse (bool): Sort in reverse order.
            page (int): Starting page. Default: 1.

        Returns:
            Page: Page iterator.
        """
        params = {"page": page}
        if q:
            params["q"] = q
        else:
            params["sort"] = sort.value
            if reverse:
                params["reverse"] = reverse

        results = []
        for page in Pages(self.client, url="projects", params=params):
            results.extend(list(page))
        return results

    def project_get(self, project_id=None):
        if project_id:
            return self._project_schema.load(
                self.client.get(f"projects/{project_id}")
            )
        else:
            return None
