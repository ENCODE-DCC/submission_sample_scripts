<?php
# PATCH an object on an ENCODE server'

#Uses Requests library from https://github.com/rmccue/Requests
include('../Requests/library/Requests.php');
Requests::register_autoloader();

# Force return from the server in JSON format
$headers = array('Content-Type' => 'application/json', 'Accept' => 'application/json');

# Authentication is always required to POST ENCODE objects
$authid = "SU45FB2Q"; // <-Replace this with your access_key
$authpw = "rae76sr5bntlz5c6"; // <-Replace this with your secret_access_key
$auth = array('auth' => array($authid, $authpw));

# This URL locates the ENCODE experiment that user can submit too 
$url ="<server>/experiments/<experiment accession/" ; // <-Replace this with appropriate server and experiment accession

# Build a array with the experiment metadata
$path_experiment= array(
	"description" => "PATCH example experiment"
);

#POST the JSON and get back response
$response = Requests::patch($url, $headers, json_encode($path_experiment), $auth);

# If the POST succeeds, the response is the new object in JSON format
var_dump($response->body);

?>