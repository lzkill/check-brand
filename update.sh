#!/bin/bash

LOCAL_FILE="$HOME/Desktop/available.html"
TEMP_FILE="/tmp/available.html"
REMOTE_USER="user"
REMOTE_HOST="host"
REMOTE_PATH="$HOME/Desktop/available.html"

inotifywait -m "$LOCAL_FILE" -e modify |
    while read path action file; do
	tac "$LOCAL_FILE" > "$TEMP_FILE"
	scp -q "$TEMP_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"
	rm -f "$TEMP_FILE"
    done
