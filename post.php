<?php
# POST an object to an ENCODE server

#Uses Requests library from https://github.com/rmccue/Requests
include('../Requests/library/Requests.php');
Requests::register_autoloader();

# Force return from the server in JSON format
$headers = array('Content-Type' => 'application/json', 'Accept' => 'application/json');

# Authentication is always required to POST ENCODE objects
$authid = "access_key"; // <-Replace this with your access_key
$authpw = "secret_access_key"; // <-Replace this with your secret_access_key
$auth = array('auth' => array($authid, $authpw));

# The URL is now the collection itself
$url = "<server>/experiments/"; // <-Replace this with appropriate server

# Build a array with the experiment metadata
$new_experiment = array(
	"description" => "POST example experiment",
	"assay_term_name" => "ChIP-seq",
	"biosample_term_name" =>"Stromal cell of bone marrow",
	"target" =>"/targets/SMAD6-human/",
	"award" => "/awards/U41HG006992/",
	"lab" => "/labs/<your-lab>/", // <-Replace this with your lab
	"references" => array (
		"PMID:19736561",
		"PMID:21913086"
	)
);

#POST the JSON and get back response
$response = Requests::post($url, $headers, json_encode($new_experiment), $auth);

# If the POST succeeds, the response is the new object in JSON format
var_dump($response->body);

?>