<?php
$ip = "mc.starforge.cz";  // Zadejte IP adresu vašeho serveru
$port = 25565;               // Zadejte správný port vašeho serveru

$socket = fsockopen($ip, $port, $errno, $errstr, 2);
if(!$socket) {
    echo "Server je offline";
} else {
    fwrite($socket, "\xFE\x01");
    $data = fread($socket, 1024);
    fclose($socket);

    if($data) {
        $data = substr($data, 9); // Odstraní první 9 znaků
        $data = explode("\x00\x00", $data);

        $num_players = $data[1];
        echo "Počet aktivních hráčů: " . $num_players;
    } else {
        echo "Nepodařilo se získat data ze serveru.";
    }
}
?>
