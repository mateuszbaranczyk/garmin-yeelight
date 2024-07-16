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
	@if [ "$$(git rev-parse @)" != "$$(git rev-parse @{u})" ]; then \
		echo "Your branch is not up to date with the remote branch."; \
		exit 1; \
	fi

push:
	git push

tag:
	@git tag -a v$(v) -m "v $(v)"
	@git push origin v$(v)

update_v:
	@echo "Updating v to $(v)"
	@sed -i '' 's/^v = ".*"/v = "$(v)"/' pyproject.toml
	@git add pyproject.toml
	@git commit -m "Bump v to $(v)"

deploy: format lint check_git push tag update_v  