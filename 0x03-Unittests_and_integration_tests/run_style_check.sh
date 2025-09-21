#!/usr/bin/env bash
# Run pycodestyle validation on all Python files

echo "Running pycodestyle checks..."
pycodestyle --max-line-length=79 .

