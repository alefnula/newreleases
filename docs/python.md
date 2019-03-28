# Using newreleases client in python scripts


To use newreleases client first you we need to instantiate the configuration.

```python
from newreleases import Config

# We can instantiate the configuration with no arguments. This will use the
# default profile from the `~/.newreleases/newreleases.ini` configuration file.
config = Config()

# We can also provide both of these parameters
config = Config(config="/path/to/my/config.ini", profile="testing")

# There is also a helper property on the Config object that returns  a
# configured client.
client = config.client
```

With the client we can do everything that we can do using the command line
utility.

#### List projects

```python
client.project_list()
```

#### Get projects
```python
client.project_get(project_id)
```

And so on... All of the client methods are documented in the API documentation.
