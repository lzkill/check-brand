#!/bin/bash

LOCAL_FILE="available.txt"
TEMP_FILE="/tmp/available.txt"
REMOTE_USER="user"
REMOTE_HOST="host"
REMOTE_PATH="~/path"

inotifywait -m "$LOCAL_FILE" -e modify |
    while read path action file; do
	tac "$LOCAL_FILE" > "$TEMP_FILE"
	scp -q "$TEMP_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"
	rm -f "$TEMP_FILE"
    done
