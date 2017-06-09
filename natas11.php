<?php

$cookie = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw=";
$known_plaintext = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));

function xor_encrypt($a, $b) {
    $key = $a;
    $text = $b;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

$decoded_cookie = base64_decode($cookie);
$key = xor_encrypt($decoded_cookie, $known_plaintext);
echo $key;

$desired_plaintext = json_encode(array("showpassword"=>"yes", "bgcolor"=>"#ffffff"));
echo "\n";
echo base64_encode(xor_encrypt($desired_plaintext, $key));

?>
