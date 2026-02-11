#!/usr/bin/env bash
set -e
python -m ruff check --fix .
python -m ruff format .
