#!/bin/bash
set -e
alembic upgrade head
python main.py
