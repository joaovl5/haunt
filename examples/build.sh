#!/bin/bash

# Simple bash script to remake build. This is terrible at the current and will be better following project updates.

rm dist/**
source ../.venv/bin/activate
hatch build dist
source .venv/bin/activate
uv pip install dist/haunt-*.whl
