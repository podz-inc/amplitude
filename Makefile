checkfiles = amplitude/ tests/
srcfiles = amplitude/
testfiles = tests/
black_opts =
py_warn = PYTHONDEVMODE=1

help:
	@echo "amplitude logger development makefile"
	@echo
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    up			Ensure dev/test dependencies are updated"
	@echo  "    deps		Ensure dev/test dependencies are installed"
	@echo  "    check		Checks that build is sane"
	@echo  "    test		Runs all tests"
	@echo  "    style		Auto-formats the code"
	@echo  "    build		Build package"

up:
	@poetry update

deps:
	@poetry install --no-root

style: deps
	@poetry run isort -src $(checkfiles)
	@poetry run black $(black_opts) $(checkfiles)

check: deps
	@poetry run black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	@poetry run flake8 $(checkfiles)

test: deps
	@$(py_warn) poetry run pytest $(testfiles)

cov: deps
	@$(py_warn) poetry run pytest $(testfiles) --cov $(srcfiles)  --cov-report html --cov-report term

cov.ci: deps
	@$(py_warn) poetry run pytest $(testfiles) --cov $(srcfiles) --cov-report xml


build: deps
	@poetry build

ci: check cov

prod.update:
	@poetry install --no-dev
