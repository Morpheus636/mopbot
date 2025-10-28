#!/bin/sh
set -e
cd /github/workspace

CONFIG_FILE="$1"
CHECK="$2"
DRY_RUN="$3"

ARGS=""

if [ -n "$CONFIG_FILE" ]; then
  ARGS="$ARGS $CONFIG_FILE"
fi

if [ "$CHECK" = "true" ]; then
  ARGS="$ARGS --check"
fi

if [ "$DRY_RUN" = "true" ]; then
  ARGS="$ARGS --dry_run"
fi

poetry --project=/app run python -m mopbot $ARGS
