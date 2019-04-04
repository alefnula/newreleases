from newreleases.schemas import ProjectSchema, ReleaseSchema

SCHEMA_MAPPING = {"projects": ProjectSchema(), "releases": ReleaseSchema()}


class Pages:
    def __init__(self, client, url, headers=None, params=None):
        """Pages iterator.

        Args:
            client (newreleases.http.HttpClient): Http client.
            url (str): API url to fetch.
            headers (Optional[dict]): Optional headers.
            params (Optional[dict]): Optional params.
        """
        self.client = client
        self.url = url
        self.headers = headers
        self.params = params or {}
        self.current_page = self.params.get("page", 1)
        self.total_pages = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.total_pages and self.current_page >= self.total_pages:
            raise StopIteration("No more pages.")

        self.params["page"] = self.current_page
        data = self.client.get(
            self.url, headers=self.headers, params=self.params
        )
        self.total_pages = data.pop("total_pages")
        self.current_page += 1

        if len(data) != 1:
            raise StopIteration("Bad data.")

        for key, value in data.items():
            return SCHEMA_MAPPING[key].load(value, many=True)
