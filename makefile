.PHONY: format lint check_git push tag update_v deploy

format:
	black .
	isort .

lint:
	flake8

check_git:
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "There are uncommitted changes. Please commit them first."; \
		exit 1; \
	fi

push:
	git push

tag:
	@git tag -a v$(v) -m "v $(v)"
	@git push origin v$(v)

update_version:
	@echo "Updating version to $(v)"
	@sed 's/^version = ".*"/version = "$(v)"/' pyproject.toml > pyproject.toml.tmp
	@mv pyproject.toml.tmp pyproject.toml
	@git add pyproject.toml
	@git commit -m "Bump version to $(v)"

deploy: format lint check_git tag update_version push