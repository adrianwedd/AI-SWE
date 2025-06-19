# Contributing Guide

This project uses pinned dependencies listed in `requirements.txt` for consistent environments.

## Setting up your environment

Before running tests or using pre-commit hooks, install the exact package versions:

```bash
pip install -r requirements.txt
```

To enable automatic checks, optionally install and configure pre-commit:

```bash
pre-commit install
```

## Running tests

After installing the dependencies, run the tests to verify your changes:

```bash
pytest --maxfail=1 --disable-warnings -q
```

