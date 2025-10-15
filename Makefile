.PHONY: lint format fix

# Targets to lint and format Python code using Ruff via uvx.
# Override PY_SRCS to narrow the scope (default: current directory).
PY_SRCS ?= .

lint:
	uvx ruff check $(PY_SRCS)
	uvx ruff format --check $(PY_SRCS)

format:
	uvx ruff format $(PY_SRCS)

fix:
	uvx ruff check $(PY_SRCS) --fix
	uvx ruff format $(PY_SRCS)
