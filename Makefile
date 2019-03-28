.PHONY: help default notebook test check format docs
.DEFAULT_GOAL := help
PROJECT := newreleases

help:                      ## Show help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


notebook:                ## Run Jupyter notebook.
	@jupyter notebook


test:                    ## Run tests.
	@py.test -n 4 --cov "$(PROJECT)"


check:                   ## Run code checks.
	@flake8 "$(PROJECT)"
	@pydocstyle "$(PROJECT)"


format:                  ## Format the code.
	@black --target-version=py37 --safe --line-length=79 "$(PROJECT)"


docs:                    ## Build documentation.
	@cd docs && make html && open _build/html/index.html
